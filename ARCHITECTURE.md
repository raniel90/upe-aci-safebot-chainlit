# 🏗️ Arquitetura do SafeBot

Este documento descreve a arquitetura técnica do SafeBot, um chatbot especializado em NR-06 construído com Chainlit e RAG.

---

## 📊 Visão Geral

```
┌────────────────────────────────────────────────────────────────┐
│                         USUÁRIO                                │
│                    (Interface Web/Chat)                        │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                      CHAINLIT LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ @on_chat_    │  │ @on_message  │  │ @on_chat_    │        │
│  │   start      │  │              │  │    end       │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
└────────────────────────────┼───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                     LANGCHAIN LAYER                            │
│  ┌────────────────────────────────────────────────────────┐   │
│  │      ConversationalRetrievalChain                      │   │
│  │                                                         │   │
│  │  ┌──────────────┐      ┌──────────────┐              │   │
│  │  │   ChatGPT    │      │  Retriever   │              │   │
│  │  │ (gpt-4o-mini)│◄────►│ (ChromaDB)   │              │   │
│  │  └──────────────┘      └──────────────┘              │   │
│  │         ▲                      ▲                       │   │
│  │         │                      │                       │   │
│  │  ┌──────┴──────────────────────┴─────────────────┐   │   │
│  │  │    ConversationBufferMemory                    │   │   │
│  │  │    (Contexto da Conversa)                      │   │   │
│  │  └────────────────────────────────────────────────┘   │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────┬───────────────────────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   OpenAI     │ │  ChromaDB    │ │   PDF NR-06  │
    │   API        │ │  Vector DB   │ │   (Source)   │
    │              │ │              │ │              │
    │ - Embeddings │ │ - Vectors    │ │ - Chunks     │
    │ - Chat       │ │ - Search     │ │ - Metadata   │
    └──────────────┘ └──────────────┘ └──────────────┘
```

---

## 🧩 Componentes Principais

### 1. Chainlit (Interface Layer)

**Função**: Gerenciar a interface de chat e interações do usuário

**Componentes**:
- `@cl.on_chat_start`: Inicialização da sessão
- `@cl.on_message`: Processamento de mensagens
- `@cl.on_chat_end`: Finalização da sessão
- `cl.user_session`: Armazenamento de estado por usuário

**Responsabilidades**:
- Renderizar interface web
- Gerenciar sessões de usuário
- Exibir mensagens com formatação Markdown
- Mostrar elementos (textos, imagens, PDFs)
- Streaming de respostas em tempo real

---

### 2. LangChain (Orchestration Layer)

**Função**: Orquestrar o fluxo de RAG e interação com LLM

#### 2.1 ConversationalRetrievalChain

Cadeia principal que integra:
- LLM (ChatGPT)
- Retriever (busca vetorial)
- Memória (contexto da conversa)

```python
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)
```

#### 2.2 ConversationBufferMemory

Mantém contexto da conversa:
- Histórico de mensagens
- Contexto acumulado
- Chave: `chat_history`

#### 2.3 Retriever

Busca semântica no ChromaDB:
- Tipo: `similarity`
- K documentos: 4 (top-4)
- Baseado em embeddings

---

### 3. Vector Database (ChromaDB)

**Função**: Armazenar e buscar chunks de documentos

**Características**:
- Embeddings via OpenAI `text-embedding-ada-002`
- Busca por similaridade semântica
- Metadados por chunk:
  ```python
  {
      "source": "NR-06",
      "page": 15,
      "document_type": "norma_regulamentadora",
      "nr_number": "06",
      "year": 2022,
      "topic": "equipamentos_protecao_individual",
      "language": "portuguese"
  }
  ```

**Persistência**: `./tmp/chromadb/`

---

### 4. OpenAI API

#### 4.1 Embeddings
- Modelo: `text-embedding-ada-002`
- Dimensão: 1536
- Uso: Vetorização de chunks do PDF

#### 4.2 Chat Completions
- Modelo: `gpt-4o-mini`
- Temperature: 0.3 (respostas mais determinísticas)
- Streaming: Habilitado
- Uso: Geração de respostas

---

### 5. Document Processing

#### 5.1 PDF Loading
```python
PyPDFLoader(PDF_PATH) → List[Document]
```

#### 5.2 Text Splitting
```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

**Estratégia**:
- Chunks de ~1000 caracteres
- Overlap de 200 para manter contexto
- Splitting recursivo (parágrafos → sentenças → palavras)

---

## 🔄 Fluxos de Dados

### Fluxo 1: Inicialização (on_chat_start)

```
1. Carregar PDF da NR-06
   ↓
2. Dividir em chunks (RecursiveCharacterTextSplitter)
   ↓
3. Criar embeddings (OpenAI)
   ↓
4. Armazenar no ChromaDB
   ↓
5. Criar ConversationalRetrievalChain
   ↓
6. Armazenar na sessão do usuário
   ↓
7. Exibir mensagem de boas-vindas
```

### Fluxo 2: Processamento de Mensagem (on_message)

```
1. Receber mensagem do usuário
   ↓
2. Recuperar chain da sessão
   ↓
3. Buscar documentos relevantes (Retriever + ChromaDB)
   │  • Top-4 chunks mais similares
   │  • Baseado em embedding da pergunta
   ↓
4. Combinar documentos + pergunta + histórico
   ↓
5. Enviar para GPT-4o-mini
   │  • System prompt: Instruções do SafeBot
   │  • Context: Chunks recuperados
   │  • History: Mensagens anteriores
   │  • Question: Pergunta atual
   ↓
6. Receber resposta (streaming)
   ↓
7. Processar source_documents
   │  • Agrupar por página
   │  • Criar elementos de texto
   ↓
8. Exibir resposta + fontes no Chainlit
   ↓
9. Atualizar memória da conversa
```

### Fluxo 3: Busca Vetorial (Retrieval)

```
Pergunta do Usuário
   ↓
Criar embedding da pergunta (OpenAI)
   ↓
Buscar por similaridade no ChromaDB
   │  • Cálculo de similaridade cosseno
   │  • Top-K chunks (K=4)
   ↓
Retornar chunks + metadados
   ↓
Usar como contexto no prompt do LLM
```

---

## 💾 Estrutura de Dados

### Chunk Document
```python
{
    "page_content": "6.1 Para os fins de aplicação...",
    "metadata": {
        "source": "NR-06",
        "page": 5,
        "document_type": "norma_regulamentadora",
        "nr_number": "06",
        "year": 2022,
        "topic": "equipamentos_protecao_individual",
        "language": "portuguese"
    }
}
```

### User Session
```python
{
    "chain": ConversationalRetrievalChain,
    "docsearch": Chroma,
}
```

### Conversation Memory
```python
{
    "chat_history": [
        HumanMessage(content="..."),
        AIMessage(content="..."),
        HumanMessage(content="..."),
        AIMessage(content="..."),
    ]
}
```

---

## 🎯 Prompts do Sistema

### System Prompt (SafeBot Instructions)

```
Você é o SafeBot, especialista em segurança e saúde do trabalho,
com foco na NR-06...

🎯 SUAS ESPECIALIDADES:
• Seleção de EPIs
• Auditoria de conformidade
• ...

[Ver código para prompt completo]
```

### Prompt RAG (Template)

```
Context: {context}
Chat History: {chat_history}
Question: {question}

[Gerado automaticamente pelo ConversationalRetrievalChain]
```

---

## 🔐 Segurança e Boas Práticas

### Segurança
- ✅ API Keys via variáveis de ambiente (`.env`)
- ✅ Sessões isoladas por usuário
- ✅ Sem armazenamento de dados sensíveis
- ✅ Validação de entrada

### Performance
- ✅ Streaming de respostas (UX melhorada)
- ✅ Cache de embeddings (ChromaDB)
- ✅ Chunks otimizados (1000 chars)
- ✅ Top-K limitado (4 documentos)

### Escalabilidade
- 🔄 ChromaDB pode ser substituído por Pinecone/Weaviate
- 🔄 Pode adicionar cache Redis para sessões
- 🔄 Pode adicionar rate limiting
- 🔄 Pode adicionar autenticação

---

## 🚀 Melhorias Futuras

### Curto Prazo
- [ ] Cache de respostas frequentes
- [ ] Métricas de uso (analytics)
- [ ] Feedback do usuário (thumbs up/down)
- [ ] Exportar conversa para PDF

### Médio Prazo
- [ ] Múltiplas NRs (NR-10, NR-12, etc.)
- [ ] Busca híbrida (keyword + semantic)
- [ ] Fine-tuning do modelo
- [ ] Autenticação de usuários

### Longo Prazo
- [ ] Integração com sistemas corporativos
- [ ] API REST para integração
- [ ] Multi-idioma
- [ ] Versão mobile (app)

---

## 📊 Métricas e Monitoramento

### Métricas Importantes
- Tempo de resposta
- Acurácia das respostas
- Satisfação do usuário
- Taxa de citações corretas
- Uso de recursos (OpenAI API)

### Logs
- Perguntas mais frequentes
- Erros e exceções
- Uso de tokens
- Documentos recuperados

---

## 🔗 Dependências Externas

| Serviço | Função | Custo | Alternativas |
|---------|--------|-------|--------------|
| OpenAI API | LLM + Embeddings | Pay-per-use | Anthropic, Cohere |
| ChromaDB | Vector DB | Gratuito | Pinecone, Weaviate, Qdrant |
| Chainlit | Interface | Gratuito | Streamlit, Gradio |

---

**🛡️ SafeBot - Arquitetura robusta e escalável para segurança do trabalho!**
