"""
SafeBot - Sistema Inteligente de Segurança do Trabalho
Chatbot especializado em NR-06 usando Chainlit e RAG
"""

import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

import chainlit as cl

# Importar autenticação
from auth import get_user_from_session, get_user_name, get_user_role

# Importar prompts personalizados por role
from prompts import (
    get_instructions_by_role,
    get_welcome_message_by_role,
    get_system_context_by_role
)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PDF_PATH = "data/pdfs/nr-06-atualizada-2022-1.pdf"

# Text splitter para documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

# NOTA: As instruções específicas por role estão agora em prompts.py
# Elas são carregadas dinamicamente baseado na role do usuário logado


async def load_pdf_knowledge_base() -> Chroma:
    """
    Carrega o PDF da NR-06 e cria a base de conhecimento vetorial
    """
    # Verificar se o arquivo existe
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            f"PDF da NR-06 não encontrado em {PDF_PATH}. "
            f"Por favor, coloque o arquivo PDF no diretório data/pdfs/"
        )
    
    # Carregar PDF
    msg = cl.Message(content="🔄 Carregando base de conhecimento da NR-06...")
    await msg.send()
    
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    
    # Adicionar metadados aos documentos
    for i, doc in enumerate(documents):
        doc.metadata = {
            "source": "NR-06",
            "document_type": "norma_regulamentadora",
            "nr_number": "06",
            "year": 2022,
            "topic": "equipamentos_protecao_individual",
            "language": "portuguese",
            "page": i + 1
        }
    
    # Dividir em chunks
    texts = text_splitter.split_documents(documents)
    
    msg.content = f"📚 Processando {len(texts)} seções do documento..."
    await msg.update()
    
    # Criar vector store
    embeddings = OpenAIEmbeddings()
    docsearch = await cl.make_async(Chroma.from_documents)(
        texts, 
        embeddings,
        collection_name="safebot_nr06",
        persist_directory="./tmp/chromadb"
    )
    
    msg.content = "✅ Base de conhecimento carregada com sucesso!"
    await msg.update()
    
    return docsearch


@cl.on_chat_start
async def start():
    """
    Inicializa o chat e carrega a base de conhecimento
    """
    # Obter usuário autenticado e sua role
    user = get_user_from_session()
    user_name = get_user_name(user) if user else "Usuário"
    user_role = get_user_role(user) if user else "user"
    
    # Obter mensagem de boas-vindas personalizada por role
    welcome_msg = get_welcome_message_by_role(user_role, user_name)
    
    await cl.Message(content=welcome_msg).send()
    
    # Carregar base de conhecimento
    try:
        docsearch = await load_pdf_knowledge_base()
    except FileNotFoundError as e:
        await cl.Message(
            content=f"⚠️ **Aviso:** {str(e)}\n\n"
                    "Você ainda pode fazer perguntas, mas as respostas não terão "
                    "a base de conhecimento da NR-06."
        ).send()
        # Criar vector store vazio como fallback
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma(
            collection_name="safebot_nr06_empty",
            embedding_function=embeddings,
            persist_directory="./tmp/chromadb"
        )
    except Exception as e:
        await cl.Message(
            content=f"❌ **Erro ao carregar base de conhecimento:** {str(e)}\n\n"
                    "Por favor, verifique sua OPENAI_API_KEY e tente novamente."
        ).send()
        return
    
    # Configurar memória da conversa
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )
    
    # Obter instruções e contexto personalizados baseados na role do usuário
    instructions = get_instructions_by_role(user_role)
    system_context = get_system_context_by_role(user_role)
    
    # Criar prompt template para QA (usando template string, não Messages)
    qa_template = f"""{instructions}

{system_context}

Use SOMENTE o contexto da NR-06 abaixo para responder à pergunta do usuário.
Se o contexto não contiver informações relevantes, diga que não sabe com base no documento.

Contexto da NR-06:
{{context}}

Histórico da conversa:
{{chat_history}}

Pergunta do usuário: {{question}}

Resposta:"""
    
    qa_prompt = ChatPromptTemplate.from_template(qa_template)
    
    # Criar chain com instruções do SafeBot
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.3,
        streaming=True,
    )
    
    # Configurar retriever com metadados
    retriever = docsearch.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 4,  # Retornar top 4 documentos mais relevantes
        }
    )
    
    # Criar chain com prompt customizado
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={"prompt": qa_prompt}
    )
    
    # Armazenar na sessão do usuário
    cl.user_session.set("chain", chain)
    cl.user_session.set("docsearch", docsearch)
    cl.user_session.set("user_role", user_role)
    cl.user_session.set("instructions", instructions)
    cl.user_session.set("system_context", system_context)


@cl.on_message
async def main(message: cl.Message):
    """
    Processa mensagens do usuário com contexto personalizado por role
    """
    # Recuperar chain e instruções da sessão
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    user_role = cl.user_session.get("user_role", "user")
    
    if not chain:
        await cl.Message(
            content="❌ **Erro:** Sessão não inicializada. Por favor, recarregue a página."
        ).send()
        return
    
    # Callback - o streaming é automático quando ChatOpenAI tem streaming=True
    cb = cl.AsyncLangchainCallbackHandler()
    
    # Processar mensagem com streaming automático
    try:
        res = await chain.acall(message.content, callbacks=[cb])
        answer = res["answer"]
        source_documents = res["source_documents"]  # type: List[Document]
        
        # Criar elementos de texto para as fontes
        text_elements = []  # type: List[cl.Text]
        
        if source_documents:
            # Agrupar fontes por página
            sources_by_page = {}
            for source_doc in source_documents:
                page = source_doc.metadata.get("page", "N/A")
                if page not in sources_by_page:
                    sources_by_page[page] = []
                sources_by_page[page].append(source_doc.page_content)
            
            # Criar elementos de texto para cada página
            for page_num, contents in sources_by_page.items():
                source_name = f"📄 NR-06 - Página {page_num}"
                combined_content = "\n\n---\n\n".join(contents)
                text_elements.append(
                    cl.Text(
                        content=combined_content, 
                        name=source_name, 
                        display="side"
                    )
                )
            
            # Adicionar referências das fontes na resposta
            source_names = [text_el.name for text_el in text_elements]
            if source_names:
                answer += f"\n\n---\n📚 **Fontes consultadas:** {', '.join(source_names)}"
        
        # Enviar resposta com fontes
        await cl.Message(content=answer, elements=text_elements).send()
        
    except Exception as e:
        await cl.Message(
            content=f"❌ **Erro ao processar sua pergunta:** {str(e)}\n\n"
                    "Por favor, tente reformular sua pergunta ou verifique "
                    "se sua OPENAI_API_KEY está configurada corretamente."
        ).send()


@cl.on_chat_end
async def end():
    """
    Finaliza a sessão de chat
    """
    await cl.Message(
        content="👋 **Obrigado por usar o SafeBot!**\n\n"
                "Lembre-se: A segurança no trabalho começa com você. "
                "Volte sempre que precisar! 🛡️"
    ).send()
