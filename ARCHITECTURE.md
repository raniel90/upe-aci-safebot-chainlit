# 🏗️ Arquitetura do SafeBot

Este documento descreve a arquitetura técnica do SafeBot, um chatbot especializado em NR-06 construído com Chainlit e RAG.

**Última atualização:** 19/11/2025  
**Versão:** 2.0 (com Autenticação e Roles)

---

## 📊 Visão Geral

```
┌────────────────────────────────────────────────────────────────┐
│                         USUÁRIO                                │
│              (Interface Web com Autenticação)                  │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                 AUTHENTICATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Password     │  │  OAuth       │  │ User Session │        │
│  │ Auth         │  │  (opcional)  │  │ Management   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│         │                  │                  │                │
│         └──────────────────┼──────────────────┘                │
└────────────────────────────┼───────────────────────────────────┘
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
│                   ROLE-BASED PROMPTS                           │
│  ┌────────────────────────────────────────────────────────┐   │
│  │      prompts.py (Sistema de Roles)                     │   │
│  │                                                         │   │
│  │  ┌──────────────┐      ┌──────────────┐              │   │
│  │  │  Supervisor  │      │  Trabalhador │              │   │
│  │  │   Prompts    │      │   Prompts    │              │   │
│  │  └──────────────┘      └──────────────┘              │   │
│  └────────────────────────────────────────────────────────┘   │
└────────────────────────────┬───────────────────────────────────┘
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

### 1. Authentication Layer (NOVO v2.0)

**Função**: Gerenciar autenticação e autorização de usuários

**Módulo**: `auth.py`

**Tipos de Autenticação Suportados**:
- **Password Authentication** (ativo): Usuário e senha
- **OAuth** (preparado): GitHub, Google, Azure AD, AWS Cognito

**Roles Disponíveis**:
- **supervisor**: Gestores de segurança do trabalho
- **user**: Trabalhadores operacionais

**Componentes**:
```python
@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]
    # Valida credenciais e retorna cl.User com metadata
    
@cl.oauth_callback  # Opcional, preparado para futuro
def oauth_callback(...)
    # Handler para autenticação OAuth

# Helper functions
get_user_from_session() -> Optional[cl.User]
get_user_role(user: cl.User) -> str
get_user_name(user: cl.User) -> str
is_supervisor(user: cl.User) -> bool
validate_user_access(user: cl.User, resource: str) -> bool
```

**Usuários Pré-configurados**:
```python
USERS_DB = {
    "supervisor": {password: "supervisor123", role: "supervisor"},
    "trabalhador": {password: "trabalhador123", role: "user"},
    "operador1": {password: "operador123", role: "user"},
    "tecnico_seguranca": {password: "tecnico123", role: "supervisor"}
}
```

---

### 2. Role-Based Prompts (NOVO v2.0)

**Função**: Fornecer instruções personalizadas por perfil de usuário

**Módulo**: `prompts.py`

**Funções principais**:
```python
get_instructions_by_role(role: str) -> str
    # Retorna instruções especializadas para cada role
    
get_welcome_message_by_role(role: str, user_name: str) -> str
    # Mensagem de boas-vindas personalizada
    
get_system_context_by_role(role: str) -> str
    # Contexto adicional específico da role
```

**Diferenças por Role**:

| Funcionalidade | Supervisor | Trabalhador |
|----------------|------------|-------------|
| Tom de linguagem | Técnico/Gerencial | Simples/Direto |
| Análise de conformidade | ✅ Completa | ❌ Não disponível |
| Geração de procedimentos | ✅ Sim | ❌ Não |
| Identificação de EPIs | ✅ Avançada | ✅ Básica |
| Relatórios de auditoria | ✅ Sim | ❌ Não |

---

### 3. Chainlit (Interface Layer)

**Função**: Gerenciar a interface de chat e interações do usuário

**Versão**: 2.0.0

**Componentes**:
- `@cl.on_chat_start`: Inicialização da sessão com autenticação
- `@cl.on_message`: Processamento de mensagens com contexto de role
- `@cl.on_chat_end`: Finalização da sessão
- `cl.user_session`: Armazenamento de estado por usuário (chain, docsearch, user_role, instructions)
- `@cl.password_auth_callback`: Validação de credenciais
- `@cl.oauth_callback`: Handler OAuth (preparado)

**Responsabilidades**:
- Renderizar interface web responsiva
- Gerenciar sessões autenticadas por usuário
- Exibir mensagens com formatação Markdown
- Mostrar elementos interativos (textos, imagens, PDFs)
- Streaming de respostas em tempo real
- Controle de acesso baseado em roles

**Recursos de UI**:
- Chat profiles (preparado para expansão)
- File upload (suportado)
- Data persistence (configurável)
- Custom CSS (`public/custom.css`)
- Logo personalizado (light/dark mode)

---

### 4. LangChain (Orchestration Layer)

**Função**: Orquestrar o fluxo de RAG e interação com LLM

**Versão**: 0.3.0

#### 4.1 ConversationalRetrievalChain

Cadeia principal que integra:
- LLM (ChatGPT)
- Retriever (busca vetorial)
- Memória (contexto da conversa)
- **Prompt Template personalizado por role**

```python
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=True,
    combine_docs_chain_kwargs={"prompt": qa_prompt}  # Personalizado por role
)
```

#### 4.2 ConversationBufferMemory

Mantém contexto da conversa:
- Histórico de mensagens por sessão
- Contexto acumulado
- Chave: `chat_history`
- Isolamento por `cl.user_session`

```python
memory = ConversationBufferMemory(
    memory_key="chat_history",
    output_key="answer",
    chat_memory=message_history,
    return_messages=True,
)
```

#### 4.3 Retriever

Busca semântica no ChromaDB:
- Tipo: `similarity`
- K documentos: 4 (top-4)
- Baseado em embeddings OpenAI
- Metadados enriquecidos

```python
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
```

---

### 5. Vector Database (ChromaDB)

**Função**: Armazenar e buscar chunks de documentos

**Versão**: 0.5.0

**Características**:
- Embeddings via OpenAI `text-embedding-ada-002`
- Busca por similaridade semântica (cosine similarity)
- Collection name: `safebot_nr06`
- Metadados enriquecidos por chunk:
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

**Capacidades**:
- Armazenamento local (desenvolvimento)
- Preparado para Chroma Cloud (produção)
- Suporte a sparse embeddings (futuro)
- Busca híbrida (keyword + semantic - futuro)

---

### 6. OpenAI API

**Versão**: 1.102.0

#### 6.1 Embeddings
- Modelo: `text-embedding-ada-002`
- Dimensão: 1536
- Uso: Vetorização de chunks do PDF
- Provider: `OpenAIEmbeddings` (LangChain)

#### 6.2 Chat Completions
- Modelo: `gpt-4o-mini`
- Temperature: 0.3 (respostas mais determinísticas)
- Streaming: Habilitado
- Uso: Geração de respostas
- Provider: `ChatOpenAI` (LangChain)

---

### 7. Document Processing

#### 7.1 PDF Loading
```python
PyPDFLoader(PDF_PATH) → List[Document]
# Carrega NR-06 atualizada 2022
```

#### 7.2 Text Splitting
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
- Metadados automáticos por chunk

---

## 🔄 Fluxos de Dados

### Fluxo 1: Autenticação e Inicialização (NEW v2.0)

```
1. Usuário acessa aplicação
   ↓
2. Chainlit exibe tela de login (@password_auth_callback)
   ↓
3. Validação de credenciais (auth.py)
   │  • Verificar USERS_DB
   │  • Retornar cl.User com metadata (role, name, provider)
   ↓
4. Criar sessão autenticada
   │  • cl.user_session.set("user", authenticated_user)
   ↓
5. Obter role do usuário
   │  • get_user_role(user) → "supervisor" ou "user"
   ↓
6. Carregar prompts personalizados (prompts.py)
   │  • get_instructions_by_role(role)
   │  • get_welcome_message_by_role(role, user_name)
   │  • get_system_context_by_role(role)
   ↓
7. Inicializar sessão de chat (@cl.on_chat_start)
   ↓
8. Carregar PDF da NR-06
   ↓
9. Dividir em chunks (RecursiveCharacterTextSplitter)
   ↓
10. Criar embeddings (OpenAI)
    ↓
11. Armazenar no ChromaDB
    ↓
12. Criar ConversationalRetrievalChain com prompt personalizado
    ↓
13. Armazenar na sessão do usuário
    │  • chain, docsearch, user_role, instructions, system_context
    ↓
14. Exibir mensagem de boas-vindas personalizada
```

### Fluxo 2: Processamento de Mensagem (on_message)

```
1. Receber mensagem do usuário
   ↓
2. Recuperar chain e role da sessão
   │  • chain = cl.user_session.get("chain")
   │  • user_role = cl.user_session.get("user_role")
   ↓
3. Buscar documentos relevantes (Retriever + ChromaDB)
   │  • Top-4 chunks mais similares
   │  • Baseado em embedding da pergunta
   │  • Filtrado por metadados (se aplicável)
   ↓
4. Combinar documentos + pergunta + histórico + prompt role-specific
   │  • Context: Chunks recuperados
   │  • Chat History: Mensagens anteriores (ConversationBufferMemory)
   │  • Question: Pergunta atual
   │  • Instructions: Instruções específicas da role
   ↓
5. Enviar para GPT-4o-mini
   │  • System prompt: Instruções do SafeBot por role
   │  • Streaming habilitado
   ↓
6. Receber resposta (streaming via AsyncLangchainCallbackHandler)
   ↓
7. Processar source_documents
   │  • Agrupar por página
   │  • Criar elementos cl.Text para exibição
   ↓
8. Exibir resposta + fontes no Chainlit
   │  • Resposta principal
   │  • Fontes consultadas (sidebar)
   ↓
9. Atualizar memória da conversa (ConversationBufferMemory)
```

### Fluxo 3: Busca Vetorial (Retrieval)

```
Pergunta do Usuário
   ↓
Criar embedding da pergunta (OpenAI text-embedding-ada-002)
   ↓
Buscar por similaridade no ChromaDB
   │  • Cálculo de similaridade cosseno
   │  • Top-K chunks (K=4)
   │  • Considerar metadados enriquecidos
   ↓
Retornar chunks + metadados
   │  • page, source, document_type, nr_number
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

### User Session (v2.0)
```python
{
    "user": cl.User,  # Usuário autenticado
    "chain": ConversationalRetrievalChain,
    "docsearch": Chroma,
    "user_role": str,  # "supervisor" ou "user"
    "instructions": str,  # Instruções específicas da role
    "system_context": str  # Contexto adicional da role
}
```

### Authenticated User
```python
cl.User(
    identifier="supervisor",
    metadata={
        "role": "supervisor",
        "name": "Gestor de Segurança",
        "provider": "credentials",  # ou "google", "github", etc
        "description": "Profissional de gestão em segurança do trabalho"
    }
)
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

## 🎯 Sistema de Prompts

### System Prompt por Role

#### **Supervisor (Gestor de Segurança)**
```
Você é o SafeBot, especialista em segurança e saúde do trabalho,
com foco na NR-06...

🎯 SUAS ESPECIALIDADES:
• Análise de conformidade normativa
• Auditoria de EPIs e procedimentos
• Geração de procedimentos técnicos
• Seleção de EPIs por risco
• Interpretação avançada da norma

🛡️ ABORDAGEM:
• Use linguagem técnica apropriada
• Cite artigos específicos da NR-06
• Forneça análises detalhadas
• Sugira melhorias e procedimentos
• Considere aspectos gerenciais
```

#### **User (Trabalhador)**
```
Você é o SafeBot, um assistente amigável de segurança do trabalho
especializado em EPIs...

🎯 SUAS ESPECIALIDADES:
• Identificação de EPIs corretos
• Explicação de uso de EPIs
• Responder dúvidas sobre proteção
• Orientação prática e simples

🛡️ ABORDAGEM:
• Use linguagem simples e direta
• Explique de forma prática
• Foque no uso correto dos EPIs
• Evite termos muito técnicos
• Seja didático e amigável
```

---

## 🔐 Segurança e Boas Práticas

### Segurança
- ✅ API Keys via variáveis de ambiente (`.env`)
- ✅ Senhas configuráveis via environment variables
- ✅ Sessões isoladas por usuário autenticado
- ✅ Sem armazenamento de dados sensíveis
- ✅ Validação de entrada
- ✅ Controle de acesso baseado em roles
- ✅ OAuth preparado para produção
- ⚠️ Em produção: usar HTTPS, rate limiting, DB para usuários

### Performance
- ✅ Streaming de respostas (UX melhorada)
- ✅ Cache de embeddings (ChromaDB persist_directory)
- ✅ Chunks otimizados (1000 chars)
- ✅ Top-K limitado (4 documentos)
- ✅ Async/await em operações I/O
- ✅ AsyncLangchainCallbackHandler para streaming

### Escalabilidade
- 🔄 ChromaDB pode ser migrado para Chroma Cloud
- 🔄 Pode adicionar cache Redis para sessões
- 🔄 Pode adicionar rate limiting
- 🔄 Sistema de roles extensível
- 🔄 Preparado para múltiplos idiomas
- 🔄 Arquitetura preparada para microserviços

---

## 🚀 Melhorias Futuras

### Curto Prazo
- [ ] Cache de respostas frequentes (Redis)
- [ ] Métricas de uso por role (analytics)
- [ ] Feedback do usuário (thumbs up/down)
- [ ] Exportar conversa para PDF
- [ ] Dashboard administrativo para gestão de usuários
- [ ] Logs de auditoria por usuário

### Médio Prazo
- [ ] Múltiplas NRs (NR-10, NR-12, NR-15, NR-17, NR-33, NR-35)
- [ ] Busca híbrida (keyword + semantic) via sparse embeddings
- [ ] Fine-tuning do modelo para terminologia de SST
- [ ] Integração com sistemas SESMT corporativos
- [ ] Migrate para Chroma Cloud (produção)
- [ ] Roles adicionais (técnico, engenheiro, auditor)
- [ ] Multi-tenancy para diferentes empresas

### Longo Prazo
- [ ] Integração com sistemas ERP/TOTVS/SAP
- [ ] API REST para integração externa
- [ ] Multi-idioma (Inglês, Espanhol)
- [ ] Versão mobile (React Native/Flutter)
- [ ] Agentes especializados por NR
- [ ] Sistema de recomendação de treinamentos
- [ ] Geração automática de relatórios CIPA
- [ ] Integração com IoT para monitoramento de EPIs

---

## 📊 Métricas e Monitoramento

### Métricas Importantes
- Tempo de resposta por query
- Acurácia das respostas (manual review)
- Satisfação do usuário por role
- Taxa de citações corretas da NR-06
- Uso de recursos OpenAI (tokens, custos)
- Usuários ativos por role
- Queries mais frequentes por perfil

### Logs Recomendados
```python
# Estrutura sugerida de logs
{
    "timestamp": "2025-11-19T10:30:00Z",
    "user_id": "supervisor",
    "user_role": "supervisor",
    "query": "Como realizar auditoria de EPIs?",
    "response_time_ms": 1250,
    "tokens_used": 450,
    "source_documents": 4,
    "satisfaction": "positive"  # via feedback
}
```

### Ferramentas Recomendadas
- **LangSmith**: Tracing de chains LangChain
- **Prometheus + Grafana**: Métricas de sistema
- **Sentry**: Error tracking
- **CloudWatch/DataDog**: Logs centralizados

---

## 🔗 Dependências e Stack Tecnológico

### Stack Completo

| Camada | Tecnologia | Versão | Função | Status |
|--------|------------|--------|--------|--------|
| **Frontend** | Chainlit | 2.0.0 | Interface de chat | ✅ Ativo |
| **Backend** | Python | 3.12 | Runtime principal | ✅ Ativo |
| **Framework IA** | LangChain | 0.3.0 | Orquestração RAG | ✅ Ativo |
| **LLM** | OpenAI GPT-4o-mini | Latest | Geração de respostas | ✅ Ativo |
| **Embeddings** | OpenAI Ada-002 | Latest | Vetorização | ✅ Ativo |
| **Vector DB** | ChromaDB | 0.5.0 | Armazenamento vetorial | ✅ Ativo |
| **PDF Processing** | PyPDF | 5.1.0 | Extração de texto | ✅ Ativo |
| **Auth** | Chainlit Auth | Built-in | Autenticação | ✅ Ativo |
| **Config** | python-dotenv | 1.0.0 | Variáveis de ambiente | ✅ Ativo |
| **Tokenization** | tiktoken | 0.8.0 | Contagem de tokens | ✅ Ativo |

### Dependências de Desenvolvimento

| Ferramenta | Versão | Função |
|------------|--------|--------|
| pytest | 7.0 | Testes unitários |
| black | 23.0 | Code formatting |
| flake8 | 6.0 | Linting |
| poetry | Latest | Gerenciamento de dependências |

### Alternativas e Migrações Futuras

| Componente Atual | Alternativas Consideradas | Quando Migrar |
|------------------|---------------------------|---------------|
| OpenAI GPT-4o-mini | Anthropic Claude, Google Gemini | Custo ou capacidades específicas |
| ChromaDB Local | Chroma Cloud, Pinecone, Weaviate, Qdrant | Produção em escala |
| Chainlit | Streamlit, Gradio, Custom React | Necessidade de UI customizada |
| Password Auth | OAuth completo, SSO, SAML | Ambiente corporativo |
| PyPDF | pypdf2, pdfplumber, unstructured | PDFs complexos |

---

## 🏗️ Arquitetura de Deploy

### Desenvolvimento (Local)
```
┌─────────────────────────────────────┐
│      Developer Machine              │
│                                     │
│  ┌──────────────┐                  │
│  │  chainlit    │ → port 8000      │
│  │  run         │                  │
│  └──────────────┘                  │
│         │                           │
│         ↓                           │
│  ┌──────────────┐                  │
│  │  ChromaDB    │ → ./tmp/chromadb │
│  │  (local)     │                  │
│  └──────────────┘                  │
│         │                           │
│         ↓                           │
│  ┌──────────────┐                  │
│  │ OpenAI API   │ → HTTPS          │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

### Produção (Docker - Recomendado)
```
┌─────────────────────────────────────────────┐
│           Cloud Provider (AWS/GCP/Azure)    │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      Docker Container               │   │
│  │                                     │   │
│  │  ┌──────────────┐                  │   │
│  │  │  Chainlit    │ → port 8000      │   │
│  │  │  App         │                  │   │
│  │  └──────────────┘                  │   │
│  │         │                           │   │
│  │         ↓                           │   │
│  │  ┌──────────────┐                  │   │
│  │  │  Volume      │                  │   │
│  │  │  /tmp/chroma │                  │   │
│  │  └──────────────┘                  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      Nginx/Load Balancer            │   │
│  │      HTTPS + SSL                    │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      External Services              │   │
│  │  - OpenAI API                       │   │
│  │  - Chroma Cloud (opcional)          │   │
│  │  - OAuth Providers                  │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Docker Compose (Disponível)
```yaml
# docker-compose.yml
services:
  safebot:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SAFEBOT_SUPERVISOR_PASSWORD=${SAFEBOT_SUPERVISOR_PASSWORD}
    volumes:
      - ./tmp/chromadb:/app/tmp/chromadb
      - ./data:/app/data
```

---

## 📚 Recursos e Documentação

### Documentação Oficial
- [Chainlit Docs](https://docs.chainlit.io/)
- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

### Documentação do Projeto
- `README.md`: Visão geral e quickstart
- `ARCHITECTURE.md`: Este documento
- `AUTHENTICATION.md`: Guia de autenticação
- `ROLES.md`: Sistema de roles
- `QUICKSTART.md`: Início rápido
- `DOCKER.md`: Deploy com Docker
- `CONTRIBUTING.md`: Guia de contribuição

---

## 🎓 Decisões Arquiteturais

### Por que Chainlit?
- ✅ Framework focado em LLM applications
- ✅ Streaming nativo
- ✅ Autenticação built-in
- ✅ UI profissional sem código frontend
- ✅ Integração perfeita com LangChain
- ✅ Deploy simples

### Por que LangChain?
- ✅ Abstração robusta para RAG
- ✅ Integrações com múltiplos providers
- ✅ Memory management built-in
- ✅ Ecosistema maduro e ativo
- ✅ Chains composables e extensíveis

### Por que ChromaDB?
- ✅ Leve e rápido para desenvolvimento
- ✅ Embeddings integrados
- ✅ Suporte a metadados rich
- ✅ Path claro para Chroma Cloud (produção)
- ✅ Open-source e gratuito

### Por que GPT-4o-mini?
- ✅ Custo-benefício excelente
- ✅ Latência baixa
- ✅ Qualidade suficiente para Q&A
- ✅ Streaming nativo
- ✅ Fallback fácil para GPT-4 se necessário

---

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente (.env)
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Chainlit
CHAINLIT_AUTH_SECRET=...
CHAINLIT_URL=http://localhost:8000

# Autenticação (Senhas)
SAFEBOT_SUPERVISOR_PASSWORD=supervisor123
SAFEBOT_USER_PASSWORD=trabalhador123
SAFEBOT_OPERADOR1_PASSWORD=operador123
SAFEBOT_TECNICO_PASSWORD=tecnico123

# OAuth (Opcional)
# OAUTH_GITHUB_CLIENT_ID=...
# OAUTH_GITHUB_CLIENT_SECRET=...
# OAUTH_GOOGLE_CLIENT_ID=...
# OAUTH_GOOGLE_CLIENT_SECRET=...
# OAUTH_COGNITO_CLIENT_ID=...
# OAUTH_COGNITO_CLIENT_SECRET=...
# OAUTH_COGNITO_DOMAIN=...

# ChromaDB
# CHROMA_API_KEY=...  # Se usar Chroma Cloud

# Ambiente
ENV=development  # development, staging, production
```

---

**🛡️ SafeBot v2.0 - Arquitetura robusta, escalável e segura para segurança do trabalho!**

---

## 🔍 Diagrama de Classes Simplificado

```
┌─────────────────┐
│   chainlit_app  │
│    (main)       │
└────────┬────────┘
         │
         ├──────────┬──────────┬──────────────┬
         ▼          ▼          ▼              ▼
    ┌────────┐ ┌────────┐ ┌─────────────┐ ┌────────┐
    │ auth   │ │prompts │ │  langchain  │ │chromadb│
    │        │ │        │ │   chains    │ │        │
    └────────┘ └────────┘ └─────────────┘ └────────┘
         │                      │              │
         ▼                      ▼              ▼
    ┌────────┐           ┌──────────┐   ┌──────────┐
    │ User   │           │ OpenAI   │   │ Vectors  │
    │Session │           │   API    │   │   DB     │
    └────────┘           └──────────┘   └──────────┘
```

---

**Última Revisão Técnica:** 19 de Novembro de 2025  
**Responsável:** SafeBot Development Team  
**Próxima Revisão:** Q1 2026
