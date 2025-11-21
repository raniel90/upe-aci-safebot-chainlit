"""
SafeBot - Sistema Inteligente de Segurança do Trabalho
Chatbot especializado em NR-06 usando Chainlit e RAG
"""

import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import Runnable, RunnablePassthrough
from langchain.schema.runnable.config import RunnableConfig
from langchain.schema import StrOutputParser
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

import chainlit as cl

# Importar autenticação
from auth import get_user_from_session, get_user_name, get_user_role

# Importar prompts personalizados por role
from prompts import (
    get_instructions_by_role,
    get_welcome_message_by_role,
    get_system_context_by_role,
)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ainda necessário para embeddings
PDF_PATH = "data/pdfs/nr-06-atualizada-2022-1.pdf"

# Text splitter para documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Aumentado para 1500 para capturar mais contexto
    chunk_overlap=300  # Aumentado para 300 para melhor continuidade entre chunks
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
            "page": i + 1,
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
        persist_directory="./tmp/chromadb",
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
            persist_directory="./tmp/chromadb",
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

    # Criar prompt template para QA (LCEL com streaming)
    qa_system_prompt = f"""{instructions}

{system_context}

Você é o SafeBot, assistente especializado em EPIs (NR-06).

REGRAS CRÍTICAS:
1. LEIA TODO O CONTEXTO abaixo antes de responder
2. Use APENAS informações do contexto fornecido
3. Se não souber: seja transparente
4. NUNCA invente informações

Use o contexto abaixo para responder à pergunta:

{{context}}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    # Criar LLM com streaming habilitado
    llm = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0.3,
        max_tokens=4096,
        streaming=True,  # Habilita streaming
        anthropic_api_key=ANTHROPIC_API_KEY,
    )

    # Configurar retriever com MMR
    retriever = docsearch.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20,
            "lambda_mult": 0.7,
        },
    )

    # Criar chain moderna com LCEL (suporta streaming nativo)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Armazenar na sessão do usuário
    cl.user_session.set("rag_chain", rag_chain)
    cl.user_session.set("message_history", message_history)
    cl.user_session.set("user_role", user_role)
    cl.user_session.set("instructions", instructions)
    cl.user_session.set("system_context", system_context)


@cl.on_message
async def main(message: cl.Message):
    """
    Processa mensagens do usuário com streaming usando LCEL
    """
    # Recuperar chain e histórico da sessão
    rag_chain = cl.user_session.get("rag_chain")
    message_history = cl.user_session.get("message_history")
    user_role = cl.user_session.get("user_role", "user")

    if not rag_chain:
        await cl.Message(
            content="❌ **Erro:** Sessão não inicializada. Por favor, recarregue a página."
        ).send()
        return

    # Preparar input com histórico de chat
    chat_history_messages = message_history.messages if message_history else []

    # Criar mensagem vazia para streaming
    msg = cl.Message(content="")
    await msg.send()

    # Processar com streaming
    try:
        # Stream a resposta
        response_text = ""
        source_documents = []

        async for chunk in rag_chain.astream(
            {
                "input": message.content,
                "chat_history": chat_history_messages,
            },
            config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            # Capturar resposta
            if "answer" in chunk:
                answer_chunk = chunk["answer"]
                response_text += answer_chunk
                await msg.stream_token(answer_chunk)
            
            # Capturar documentos de contexto
            if "context" in chunk:
                source_documents = chunk["context"]

        # Adicionar mensagens ao histórico
        message_history.add_user_message(message.content)
        message_history.add_ai_message(response_text)

        # Criar elementos de texto para as fontes
        text_elements = []

        if source_documents:
            # Remover conteúdos duplicados (chunks iguais)
            unique_documents = []
            seen_contents = set()
            for doc in source_documents:
                content_key = doc.page_content.strip()
                if content_key not in seen_contents:
                    seen_contents.add(content_key)
                    unique_documents.append(doc)
            source_documents = unique_documents

            # Agrupar fontes por página
            sources_by_page = {}
            for source_doc in source_documents:
                page = source_doc.metadata.get("page", "N/A")
                source_label = source_doc.metadata.get("source", "Documento")
                key = (source_label, page)
                if key not in sources_by_page:
                    sources_by_page[key] = []
                if source_doc.page_content not in sources_by_page[key]:
                    sources_by_page[key].append(source_doc.page_content)

            # Criar elementos de texto para cada página
            for (source_label, page_num), contents in sources_by_page.items():
                source_name = f"📄 {source_label} - Página {page_num}"
                combined_content = "\n\n---\n\n".join(contents)
                text_elements.append(
                    cl.Text(content=combined_content, name=source_name, display="side")
                )

            # Adicionar referências das fontes
            source_names = [text_el.name for text_el in text_elements]
            if source_names:
                footer = f"\n\n---\n📚 **Fontes consultadas:** {', '.join(source_names)}"
                await msg.stream_token(footer)

        # Atualizar mensagem final com elementos
        msg.elements = text_elements
        await msg.update()

    except Exception as e:
        await cl.Message(
            content=f"❌ **Erro ao processar sua pergunta:** {str(e)}\n\n"
            "Por favor, tente reformular sua pergunta ou verifique "
            "se sua ANTHROPIC_API_KEY está configurada corretamente."
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
