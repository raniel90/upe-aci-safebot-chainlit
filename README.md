# 🛡️ SafeBot - Sistema Inteligente de Segurança do Trabalho

> Chatbot especializado em NR-06 (Equipamentos de Proteção Individual) construído com Chainlit, LangChain e RAG (Retrieval Augmented Generation)

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Chainlit](https://img.shields.io/badge/Chainlit-2.0+-green.svg)](https://chainlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Características](#características)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Referências](#referências)

---

## 🎯 Sobre o Projeto

O **SafeBot** é um assistente virtual inteligente especializado em **Segurança e Saúde do Trabalho**, com foco específico na **NR-06** (Norma Regulamentadora sobre Equipamentos de Proteção Individual).

Este projeto utiliza técnicas avançadas de **RAG (Retrieval Augmented Generation)** para fornecer respostas precisas e fundamentadas com base na legislação oficial, combinando:

- 🤖 **LLMs (Large Language Models)** - GPT-4o-mini da OpenAI
- 📚 **Base de Conhecimento Vetorial** - ChromaDB com embeddings
- 💬 **Interface de Chat Moderna** - Chainlit
- 🔍 **Busca Semântica** - Recuperação inteligente de documentos

### 🌟 Diferenciais

Este projeto foi desenvolvido utilizando as **melhores práticas de prompt engineering** e **estratégias avançadas de RAG** para proporcionar uma experiência de chat moderna e intuitiva com o framework **Chainlit**.

---

## ✨ Características

### 🎯 Especialidades do SafeBot

- 🛡️ **Seleção de EPIs** - Recomendações adequadas por tipo de risco
- 📋 **Auditoria de Conformidade** - Checklists e análises de conformidade
- 🎓 **Treinamentos** - Criação de programas de capacitação personalizados
- 🔍 **Investigação de Acidentes** - Análise de incidentes relacionados a EPIs
- ⚖️ **Consultoria Legal** - Esclarecimento de aspectos legais da NR-06
- 📝 **Geração de POPs** - Procedimentos operacionais padrão

### 💡 Recursos Técnicos

- ✅ **RAG com ChromaDB** - Base de conhecimento vetorial persistente
- ✅ **Memória de Conversação** - Contexto mantido durante toda a sessão
- ✅ **Streaming de Respostas** - Respostas progressivas em tempo real
- ✅ **Citação de Fontes** - Referências diretas à NR-06 com número de páginas
- ✅ **Interface Moderna** - UI responsiva e amigável do Chainlit
- ✅ **Markdown Rico** - Formatação avançada com emojis e estrutura clara
- ✅ **Autenticação** - Login por senha e preparado para OAuth (GitHub, Google, Azure AD)

---

## 🏗️ Arquitetura

```
┌─────────────────┐
│  Usuário (Chat) │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│   Chainlit UI       │
│  (Interface Chat)   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   LangChain                     │
│   ┌─────────────────────────┐   │
│   │ ConversationalRetrieval │   │
│   │        Chain            │   │
│   └───────┬─────────────────┘   │
│           │                     │
│    ┌──────▼──────┐              │
│    │   Memory    │              │
│    │  (Context)  │              │
│    └─────────────┘              │
└────────┬────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ OpenAI  │ │  ChromaDB    │
│ GPT-4o  │ │  (Vector DB) │
│  mini   │ │              │
└─────────┘ └──────┬───────┘
                   │
                   ▼
            ┌─────────────┐
            │  PDF NR-06  │
            │  (Embeddings)│
            └─────────────┘
```

### 🔄 Fluxo de Processamento

1. **Usuário** envia uma pergunta via interface Chainlit
2. **LangChain** processa a pergunta e busca no **ChromaDB**
3. **ChromaDB** retorna os trechos mais relevantes da NR-06
4. **GPT-4o-mini** gera uma resposta usando o contexto recuperado
5. **Chainlit** exibe a resposta com citações de fontes
6. **Memória** mantém o contexto da conversa

---

## 🚀 Instalação

> 💡 **Instalando no Ubuntu?** Consulte o guia detalhado: [INSTALL_UBUNTU.md](INSTALL_UBUNTU.md)

### 📋 Pré-requisitos

- Python 3.12 ou superior
- Poetry (gerenciador de dependências)
- Chave de API da OpenAI

### 🔧 Passo a Passo

1. **Clone o repositório:**

```bash
git clone https://github.com/raniel90/upe-aci-safebot-chainlit.git
cd upe-aci-safebot-chainlit
```

2. **Instale as dependências com Poetry:**

```bash
poetry install
```

3. **Configure suas variáveis de ambiente:**

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave da OpenAI
nano .env  # ou use seu editor preferido
```

No arquivo `.env`, configure:

```env
# OpenAI (obrigatório)
OPENAI_API_KEY=sk-sua-chave-aqui

# Autenticação (recomendado - mude as senhas!)
SAFEBOT_ADMIN_PASSWORD=sua-senha-admin-segura
SAFEBOT_USER_PASSWORD=sua-senha-usuario-segura
CHAINLIT_AUTH_SECRET=seu-secret-muito-seguro-aqui
```

4. **Verifique se o PDF da NR-06 está presente:**

```bash
ls -lh data/pdfs/nr-06-atualizada-2022-1.pdf
```

Se não estiver, coloque o arquivo PDF da NR-06 no diretório `data/pdfs/`.

---

## 💬 Como Usar

### 🎬 Iniciar o Chat

```bash
# Ativar o ambiente virtual do Poetry
poetry shell

# Executar o aplicativo
chainlit run chainlit_app.py
```

O chat será aberto automaticamente no navegador em `http://localhost:8000`

### 🔐 Login

Na primeira vez, você verá uma tela de login. Escolha um perfil para testar:

**👷 Trabalhador (Linguagem Simples):**
- **Usuário**: `trabalhador`
- **Senha**: `trabalhador123`

**👔 Supervisor (Linguagem Técnica):**
- **Usuário**: `supervisor`
- **Senha**: `supervisor123`

⚠️ **Importante**: Altere as senhas padrão antes de usar em produção!

📚 **Guias completos:**
- [AUTHENTICATION.md](AUTHENTICATION.md) - Configuração de autenticação
- [ROLES.md](ROLES.md) - Sistema de perfis e personalização
- [QUICKSTART_ROLES.md](QUICKSTART_ROLES.md) - Teste rápido dos perfis

### 📱 Exemplos de Perguntas

Experimente fazer perguntas como:

```
🔹 "Quais EPIs são obrigatórios para trabalho em altura?"
🔹 "Como fazer uma auditoria de conformidade de EPIs?"
🔹 "Qual a responsabilidade do empregador segundo a NR-06?"
🔹 "Quais são os tipos de luvas de proteção?"
🔹 "Como deve ser feito o treinamento de uso de EPIs?"
🔹 "Quais são as penalidades por não fornecer EPIs adequados?"
```

### 🎯 Recursos da Interface

- **📚 Fontes Citadas**: Visualize os trechos da NR-06 usados na resposta
- **💬 Histórico de Conversa**: O bot lembra do contexto anterior
- **📄 Páginas Referenciadas**: Veja exatamente de onde vem cada informação
- **⚡ Streaming**: Respostas aparecem progressivamente
- **🎨 Formatação Rica**: Markdown, emojis e estrutura clara

---

## 📁 Estrutura do Projeto

```
safebot-chainlit/
├── chainlit_app.py          # Aplicação principal do Chainlit
├── auth.py                  # Módulo de autenticação
├── prompts.py               # Prompts personalizados por role
├── pyproject.toml            # Configuração do Poetry e dependências
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Este arquivo
├── AUTHENTICATION.md        # Guia completo de autenticação
├── ROLES.md                 # Sistema de perfis e personalização
├── QUICKSTART_ROLES.md      # Teste rápido dos perfis
│
├── .chainlit/
│   └── config.toml          # Configuração do Chainlit
│
├── data/
│   └── pdfs/
│       └── nr-06-atualizada-2022-1.pdf  # PDF da NR-06
│
└── tmp/
    └── chromadb/            # Base de conhecimento vetorial (criada automaticamente)
```

---

## 🧠 Tecnologias e Referências

### 🔗 Stack Tecnológico

- [Chainlit](https://chainlit.io) - Framework de chat conversacional
- [LangChain](https://langchain.com) - Framework para aplicações LLM
- [ChromaDB](https://www.trychroma.com/) - Banco de dados vetorial
- [OpenAI GPT-4o](https://openai.com) - Modelo de linguagem
- [PyPDF](https://pypdf.readthedocs.io/) - Processamento de PDFs

### 📖 Documentação Oficial

- **NR-06**: [Ministério do Trabalho](https://www.gov.br/trabalho-e-previdencia/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/seguranca-e-saude-no-trabalho/ctpp-nrs/norma-regulamentadora-no-6-nr-6)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. 🐛 Reportar bugs
2. 💡 Sugerir novas funcionalidades
3. 🔧 Melhorar o código
4. 📝 Aprimorar a documentação

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Autores

Desenvolvido como parte do projeto de pesquisa em IA e Segurança do Trabalho.

**SafeBot Team** - Universidade Federal

---

## 🙏 Agradecimentos

- À comunidade **Chainlit** pelo framework incrível
- Ao **LangChain** pela facilidade de integração
- À **OpenAI** pelos modelos de linguagem avançados
- Aos profissionais de Segurança do Trabalho que inspiram este projeto

---

<div align="center">

**🛡️ SafeBot - Porque segurança no trabalho é coisa séria!**

[⬆ Voltar ao topo](#-safebot---sistema-inteligente-de-segurança-do-trabalho)

</div>
