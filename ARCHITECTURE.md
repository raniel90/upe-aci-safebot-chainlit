# 🏗️ Arquitetura do SafeBot

**Versão:** 3.0  
**Última atualização:** 20/11/2025  
**Status:** Produção

---

## 📋 Visão Geral

SafeBot é um assistente conversacional especializado em NR-06 (Equipamentos de Proteção Individual) que utiliza Retrieval-Augmented Generation (RAG) para fornecer informações precisas e contextualizadas baseadas na norma regulamentadora.

### Tecnologias Principais

- **Frontend**: Chainlit 2.0 (Web Interface)
- **LLM**: Claude Sonnet 4.5 (Anthropic)
- **Embeddings**: text-embedding-ada-002 (OpenAI)
- **Vector Database**: ChromaDB 0.5
- **Orchestration**: LangChain 0.3 (LCEL)
- **Authentication**: Chainlit Auth (Password + OAuth)

---

## 🏛️ Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────────┐
│                      CAMADA DE APRESENTAÇÃO                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Chainlit Web Interface                       │  │
│  │  • Chat UI                                           │  │
│  │  • Autenticação (Password/OAuth)                     │  │
│  │  • Streaming em tempo real                           │  │
│  │  • Gestão de sessões                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE LÓGICA                         │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Sistema de Roles                             │  │
│  │  • Supervisor (Técnico/Gerencial)                    │  │
│  │  • Trabalhador (Simples/Prático)                     │  │
│  │  • Prompts personalizados por perfil                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                            ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         LangChain LCEL Orchestration                 │  │
│  │  • RAG Chain (Retrieval + Generation)                │  │
│  │  • Gestão de contexto conversacional                 │  │
│  │  • Streaming de respostas                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE DADOS                          │
│                                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────┐  │
│  │ ChromaDB │    │ Claude   │    │ OpenAI Embeddings    │  │
│  │ Vector   │←→  │ Sonnet   │    │ text-embedding-ada   │  │
│  │ Store    │    │ 4.5      │    │                      │  │
│  └──────────┘    └──────────┘    └──────────────────────┘  │
│       ↑                                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         PDF Source (NR-06)                           │  │
│  │  • Chunks de 1500 caracteres                         │  │
│  │  • Overlap de 300 caracteres                         │  │
│  │  • Metadados enriquecidos                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Componentes Arquiteturais

### 1. Interface & Autenticação

**Responsabilidade**: Gerenciar interação com usuário e controle de acesso

**Características**:
- Interface web responsiva com chat em tempo real
- Autenticação via credenciais (password-based)
- Suporte preparado para OAuth (Google, GitHub, Azure AD)
- Gestão de sessões isoladas por usuário
- Streaming de respostas palavra por palavra

**Controle de Acesso**:
- **Supervisor**: Gestores de segurança do trabalho
- **Trabalhador**: Usuários operacionais do chão de fábrica

---

### 2. Sistema de Roles

**Responsabilidade**: Personalizar experiência baseada no perfil do usuário

**Diferenciação**:

| Aspecto | Supervisor | Trabalhador |
|---------|-----------|-------------|
| Linguagem | Técnica/Formal | Simples/Direta |
| Citações | Artigos e páginas específicas | Linguagem natural |
| Análise | Detalhada com POPs/auditorias | Prática e objetiva |
| Formatação | Estruturada | Fluida e concisa |
| Foco | Gestão e conformidade | Uso correto de EPIs |

**Implementação**: 
- Prompts específicos por role
- Mensagens de boas-vindas personalizadas
- Contexto adicional diferenciado

---

### 3. RAG (Retrieval-Augmented Generation)

**Responsabilidade**: Combinar busca semântica com geração de linguagem natural

#### 3.1 Retrieval (Busca)

**Estratégia**: MMR (Maximum Marginal Relevance)
- Busca 20 chunks candidatos por similaridade
- Seleciona 5 mais diversos (evita redundância)
- Balance: 70% relevância + 30% diversidade

**Vector Store**: ChromaDB
- Embeddings: OpenAI text-embedding-ada-002 (1536 dimensões)
- Busca por similaridade de cosseno
- Metadados: página, source, tipo de documento, ano

#### 3.2 Generation (Geração)

**LLM**: Claude Sonnet 4.5
- Contexto: 200k tokens
- Temperatura: 0.3 (respostas determinísticas)
- Max tokens: 4096
- Streaming: habilitado nativamente

**Por que Claude?**
- Melhor aderência a instruções complexas
- Menor taxa de alucinação
- Mais conservador e factual
- Suporte nativo a streaming com LCEL

---

### 4. Processamento de Documentos

**Pipeline**:

```
PDF (NR-06) → Extração de Texto → Chunking → Embeddings → Vector Store
```

**Chunking**:
- Tamanho: 1500 caracteres
- Overlap: 300 caracteres (20%)
- Estratégia: RecursiveCharacterTextSplitter
- Objetivo: Capturar artigos completos com contexto

**Metadados por Chunk**:
- source: "NR-06"
- page: número da página
- document_type: "norma_regulamentadora"
- nr_number: "06"
- year: 2022
- topic: "equipamentos_protecao_individual"
- language: "portuguese"

---

### 5. Orquestração (LangChain LCEL)

**Responsabilidade**: Coordenar fluxo entre retrieval, LLM e memória

**Padrão**: LCEL (LangChain Expression Language)
- Composição declarativa de componentes
- Streaming nativo end-to-end
- Gestão automática de contexto conversacional

**Componentes**:
1. **Retriever**: Busca chunks relevantes via MMR
2. **Prompt Template**: Personalizado por role
3. **LLM**: Claude Sonnet 4.5 com streaming
4. **Memory**: ChatMessageHistory para contexto

**Vantagens sobre chains legadas**:
- Streaming funciona nativamente
- Mais flexível e componível
- Melhor performance
- Código mais limpo

---

## 🔄 Fluxo de Interação

### Jornada de uma Pergunta

```
1. USUÁRIO
   ↓ Faz pergunta
   
2. AUTENTICAÇÃO
   ↓ Valida sessão e role
   
3. RETRIEVAL
   ↓ Busca 5 chunks mais relevantes (MMR)
   
4. CONTEXTO
   ↓ Monta prompt com:
   ↓ • System prompt (personalizado por role)
   ↓ • Histórico da conversa
   ↓ • Chunks recuperados (contexto)
   ↓ • Pergunta do usuário
   
5. GERAÇÃO (STREAMING)
   ↓ Claude gera resposta token por token
   ↓ Token 1 → Token 2 → Token 3 → ...
   
6. APRESENTAÇÃO
   ↓ UI exibe resposta em tempo real
   ↓ Adiciona fontes consultadas
   
7. HISTÓRICO
   ↓ Salva pergunta + resposta na memória
```

---

## 📊 Características Técnicas

### Performance

- **TTFB (Time To First Byte)**: ~1-2 segundos
- **Streaming**: Resposta visível em tempo real
- **Latência total**: 5-10 segundos (dependendo da complexidade)
- **Chunks recuperados**: 5 por consulta
- **Contexto conversacional**: Mantido por sessão

### Escalabilidade

- **Vector Store**: ChromaDB (local para dev, Chroma Cloud para prod)
- **Sessões**: Isoladas por usuário via Chainlit
- **Autenticação**: Preparado para OAuth e integrações enterprise
- **Deployment**: Docker + Docker Compose

### Segurança

- **Autenticação**: Obrigatória para acesso
- **Isolamento**: Sessões independentes por usuário
- **API Keys**: Gerenciadas via variáveis de ambiente
- **RBAC**: Role-Based Access Control (supervisor vs trabalhador)

---

## 🚀 Decisões Arquiteturais

### 1. Claude Sonnet 4.5 vs GPT-4o-mini

**Decisão**: Claude Sonnet 4.5

**Justificativa**:
- Melhor aderência a instruções complexas
- Menor taxa de alucinação (crítico para segurança do trabalho)
- Streaming nativo com LCEL
- Contexto maior (200k vs 128k tokens)
- Mais conservador (não inventa informações)

**Trade-off**: Custo ligeiramente maior, mas compensado pela qualidade

---

### 2. MMR vs Similarity Search

**Decisão**: MMR (Maximum Marginal Relevance)

**Justificativa**:
- Elimina chunks duplicados/redundantes
- Maior diversidade de informação
- Melhor cobertura do documento
- Respostas mais completas

**Trade-off**: ~20% mais lento, mas qualidade superior

---

### 3. LCEL vs ConversationalRetrievalChain

**Decisão**: LCEL (LangChain Expression Language)

**Justificativa**:
- Streaming nativo funcionando
- Mais moderno e mantido
- Maior flexibilidade
- Melhor performance
- Código mais limpo

**Trade-off**: Requer mais código manual, mas maior controle

---

### 4. Chunks de 1500 caracteres

**Decisão**: 1500 chars (overlap 300)

**Justificativa**:
- Captura artigos completos da NR-06
- Melhor contexto para perguntas complexas
- Menos fragmentação
- Overlap suficiente para continuidade

**Trade-off**: Menos chunks totais, mas mais contexto por chunk

---

## 🎨 Padrões de Design

### Separation of Concerns

- **Presentation**: Chainlit (UI + Sessões)
- **Business Logic**: Prompts + RAG orchestration
- **Data**: ChromaDB + PDF source

### Dependency Injection

- Componentes (LLM, Retriever, Memory) injetados na chain
- Facilita testes e substituição de componentes

### Strategy Pattern

- Prompts diferentes por role (Supervisor vs Trabalhador)
- Comportamento alterado em runtime baseado no usuário

### Chain of Responsibility

- Retrieval → Contexto → LLM → Resposta
- Cada componente processa e passa para o próximo

---

## 📦 Dependências Principais

| Categoria | Tecnologia | Versão | Uso |
|-----------|-----------|--------|-----|
| Framework | Chainlit | 2.0.0 | Interface & Auth |
| LLM | Claude (Anthropic) | 0.40.0 | Geração de respostas |
| Embeddings | OpenAI | 1.102.0 | Vetorização |
| Orchestration | LangChain | 0.3.0 | RAG pipeline |
| Vector DB | ChromaDB | 0.5.0 | Busca semântica |
| PDF Processing | PyPDF | 5.1.0 | Extração de texto |

---

## 🔐 Variáveis de Ambiente

```
ANTHROPIC_API_KEY    # Claude API key
OPENAI_API_KEY       # OpenAI Embeddings
CHAINLIT_AUTH_SECRET # Segredo de autenticação
```

---

## 📁 Estrutura de Arquivos

```
safebot-chainlit/
├── chainlit_app.py          # Aplicação principal
├── auth.py                  # Autenticação e roles
├── prompts.py               # Prompts por role
├── data/pdfs/               # PDF da NR-06
├── tmp/chromadb/            # Vector store local
├── public/                  # Assets (logos, CSS)
└── pyproject.toml           # Dependências
```

---

## 🎯 Casos de Uso Suportados

### Trabalhador (User)

- Identificar EPIs necessários para atividade
- Entender como usar EPIs corretamente
- Verificar direitos sobre fornecimento de EPIs
- Saber quando trocar/solicitar EPIs
- Reportar problemas com EPIs

### Supervisor (Gestor)

- Interpretar artigos técnicos da NR-06
- Elaborar POPs e procedimentos
- Realizar auditorias de conformidade
- Analisar responsabilidades legais
- Gerar documentação técnica
- Avaliar riscos e medidas de controle

---

## 🔮 Extensibilidade

### Preparado Para:

- **Multi-tenancy**: Separação por empresa/organização
- **Outras NRs**: Arquitetura suporta múltiplos documentos
- **OAuth Providers**: Google, GitHub, Azure AD, AWS Cognito
- **Cloud Deployment**: Chroma Cloud, AWS, Azure, GCP
- **Analytics**: Tracking de perguntas e qualidade de respostas
- **Feedback Loop**: Sistema de avaliação de respostas

---

## 📚 Documentação Relacionada

- `AUTHENTICATION.md` - Detalhes de autenticação e roles
- `ROLES.md` - Sistema de roles e personalização
- `DOCKER.md` - Deployment com containers
- `QUICKSTART.md` - Guia de início rápido

---

**Versão**: 3.0  
**Mantido por**: Equipe SafeBot  
**Última revisão**: 20/11/2025
