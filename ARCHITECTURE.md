# 🏗️ Arquitetura do SafeBot

**Versão:** 1.0  
**Última atualização:** 20/11/2025  
**Status:** Produção

---

## Visão Geral

SafeBot é um assistente conversacional especializado em normas regulamentadoras de segurança do trabalho que utiliza Retrieval-Augmented Generation (RAG) para fornecer informações precisas e contextualizadas baseadas nas normas oficiais.

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
│                      CAMADA DE APRESENTAÇÃO                 │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Chainlit Web Interface                       │   │
│  │  • Chat UI                                           │   │
│  │  • Autenticação (Password/OAuth)                     │   │
│  │  • Streaming em tempo real                           │   │
│  │  • Gestão de sessões                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE LÓGICA                        │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Sistema de Roles                             │   │
│  │  • Supervisor (Técnico/Gerencial)                    │   │
│  │  • Trabalhador (Simples/Prático)                     │   │
│  │  • Prompts personalizados por perfil                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↓                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         LangChain LCEL Orchestration                 │   │
│  │  • RAG Chain (Retrieval + Generation)                │   │
│  │  • Gestão de contexto conversacional                 │   │
│  │  • Streaming de respostas                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE DADOS                         │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────┐   │
│  │ ChromaDB │    │ Claude   │    │ OpenAI Embeddings    │   │
│  │ Vector   │←→  │ Sonnet   │    │ text-embedding-ada   │   │
│  │ Store    │    │ 4.5      │    │                      │   │
│  └──────────┘    └──────────┘    └──────────────────────┘   │
│       ↑                                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         PDF Source (NR-06)                           │   │
│  │  • Chunks de 1500 caracteres                         │   │
│  │  • Overlap de 300 caracteres                         │   │
│  │  • Metadados enriquecidos                            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Componentes Arquiteturais

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
| Foco | Gestão e conformidade | Uso correto e segurança |

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
PDFs (Normas) → Extração de Texto → Chunking → Embeddings → Vector Store
```

**Chunking**:
- Tamanho: 1500 caracteres
- Overlap: 300 caracteres (20%)
- Estratégia: RecursiveCharacterTextSplitter
- Objetivo: Capturar artigos completos com contexto

**Metadados por Chunk**:
- source: identificação da norma (ex: "NR-06")
- page: número da página
- document_type: "norma_regulamentadora"
- nr_number: número da NR
- year: ano da versão
- topic: tema da norma
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

## Fluxo de Interação

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

## Características Técnicas

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

## Decisões Arquiteturais

### 1. Large Language Model

**Escolha**: Claude Sonnet 4.5 (Anthropic)

**Justificativa**:
- Excelente aderência a instruções complexas
- Baixa taxa de alucinação (crítico para contextos regulamentadores)
- Streaming nativo com LCEL
- Contexto de 200k tokens
- Conservador e factual

---

### 2. Estratégia de Retrieval

**Escolha**: MMR (Maximum Marginal Relevance)

**Justificativa**:
- Elimina chunks duplicados
- Maior diversidade de informação
- Melhor cobertura do documento
- Respostas mais completas

**Configuração**: fetch_k=20, k=5, lambda_mult=0.7

---

### 3. Orquestração

**Escolha**: LCEL (LangChain Expression Language)

**Justificativa**:
- Streaming nativo funcionando
- Padrão moderno e mantido
- Maior flexibilidade
- Melhor performance
- Componibilidade

---

### 4. Configuração de Chunks

**Escolha**: 1500 caracteres (overlap 300)

**Justificativa**:
- Captura artigos completos das normas
- Melhor contexto para perguntas complexas
- Menos fragmentação de conteúdo
- Overlap suficiente para continuidade entre chunks

---

## Padrões de Design

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

## Dependências Principais

| Categoria | Tecnologia | Versão | Uso |
|-----------|-----------|--------|-----|
| Framework | Chainlit | 2.0.0 | Interface & Auth |
| LLM | Claude (Anthropic) | 0.40.0 | Geração de respostas |
| Embeddings | OpenAI | 1.102.0 | Vetorização |
| Orchestration | LangChain | 0.3.0 | RAG pipeline |
| Vector DB | ChromaDB | 0.5.0 | Busca semântica |
| PDF Processing | PyPDF | 5.1.0 | Extração de texto |

---

## Casos de Uso Suportados

### Trabalhador (User)

- Identificar equipamentos de proteção necessários
- Entender como usar equipamentos corretamente
- Verificar direitos sobre fornecimento
- Saber quando trocar/solicitar equipamentos
- Reportar problemas ou não conformidades

### Supervisor (Gestor)

- Interpretar artigos técnicos das normas
- Elaborar POPs e procedimentos
- Realizar auditorias de conformidade
- Analisar responsabilidades legais
- Gerar documentação técnica
- Avaliar riscos e medidas de controle