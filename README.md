# 🛡️ SafeBot - Assistente de Segurança do Trabalho

> Assistente conversacional inteligente para normas regulamentadoras de segurança do trabalho

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Chainlit](https://img.shields.io/badge/Chainlit-2.0+-green.svg)](https://chainlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## O que é o SafeBot?

SafeBot é um assistente virtual que responde perguntas sobre normas regulamentadoras de segurança do trabalho utilizando **RAG (Retrieval-Augmented Generation)** para fornecer respostas precisas baseadas nos documentos oficiais.

### Características Principais

- **Streaming em tempo real** - Respostas aparecem palavra por palavra
- **Respostas fundamentadas** - Baseadas nos documentos oficiais das normas
- **Perfis personalizados** - Linguagem adaptada para trabalhador ou supervisor
- **Fontes citadas** - Referências diretas às páginas consultadas
- **Memória conversacional** - Mantém contexto da conversa
- **Autenticação integrada** - Controle de acesso por perfil

---

## 🚀 Início Rápido

### Opção 1: Docker (Recomendado)

```bash
docker-compose up
```

Acesse: `http://localhost:8000`

**Detalhes**: Ver [DOCKER.md](DOCKER.md)

### Opção 2: Local com Poetry

```bash
# 1. Instalar dependências
poetry install

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env e adicione suas API keys

# 3. Rodar aplicação
poetry run chainlit run chainlit_app.py
```

**Detalhes**: Ver [QUICKSTART.md](QUICKSTART.md)

---

## 🔐 Login

Escolha seu perfil:

| Perfil | Usuário | Senha | Linguagem |
|--------|---------|-------|-----------|
| Trabalhador | `trabalhador` | `trabalhador123` | Simples/Prática |
| Supervisor | `supervisor` | `supervisor123` | Técnica/Gerencial |

⚠️ **Altere as senhas padrão em produção!**

---

## 💬 Exemplos de Uso

### Perguntas de Trabalhadores

```
"Quem deve fornecer os equipamentos de proteção?"
"A empresa pode cobrar pelos equipamentos?"
"Meu capacete está rachado, o que fazer?"
```

### Perguntas de Supervisores

```
"Quais as responsabilidades legais do empregador?"
"Como elaborar um POP para controle de EPIs?"
"Que documentação é obrigatória para conformidade?"
```

---

## 📖 Documentação

| Documento | Conteúdo |
|-----------|----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura técnica do sistema |
| [AUTHENTICATION.md](AUTHENTICATION.md) | Configuração de autenticação |
| [ROLES.md](ROLES.md) | Sistema de perfis de usuário |
| [DOCKER.md](DOCKER.md) | Deploy com Docker |
| [QUICKSTART.md](QUICKSTART.md) | Guia de início rápido |
| [CUSTOMIZATION.md](CUSTOMIZATION.md) | Personalização do SafeBot |

---

## 🛠️ Requisitos Técnicos

### API Keys Necessárias

- **ANTHROPIC_API_KEY** - Claude Sonnet 4.5 (geração de respostas)
- **OPENAI_API_KEY** - OpenAI Embeddings (vetorização)

### Dependências Principais

- Python 3.12+
- Chainlit 2.0
- LangChain 0.3
- ChromaDB 0.5
- Anthropic SDK 0.40
- OpenAI SDK 1.102

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# APIs
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
OPENAI_API_KEY=sk-xxxxx

# Autenticação
CHAINLIT_AUTH_SECRET=seu-secret-seguro
SAFEBOT_ADMIN_PASSWORD=senha-admin
SAFEBOT_USER_PASSWORD=senha-usuario
```

### Modo Desenvolvimento

```bash
# Com live reload e debug
poetry run chainlit run chainlit_app.py -w -d
```

---

## 📁 Estrutura de Arquivos

```
safebot-chainlit/
├── chainlit_app.py      # Aplicação principal
├── auth.py              # Autenticação e roles
├── prompts.py           # Prompts personalizados
├── pyproject.toml       # Dependências
├── data/pdfs/           # Normas regulamentadoras (PDFs)
└── tmp/chromadb/        # Vector store (gerado automaticamente)
```

---

## 🔧 Solução de Problemas

### Erro: Module not found

```bash
poetry install
```

### Erro: ChromaDB vazio

```bash
rm -rf tmp/chromadb
# Reinicie a aplicação para recriar
```

### Erro: API Key inválida

Verifique se as chaves no `.env` estão corretas:
- `ANTHROPIC_API_KEY` para Claude
- `OPENAI_API_KEY` para embeddings

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Abra um Pull Request

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

---

## 📄 Licença

Este projeto está sob a licença MIT. Ver [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- Comunidade **Chainlit** pelo framework de chat
- **LangChain** pela orquestração de RAG
- **Anthropic** pelo Claude Sonnet 4.5
- **OpenAI** pelos embeddings de alta qualidade
- Profissionais de Segurança do Trabalho que inspiram este projeto

---

<div align="center">

**🛡️ SafeBot - Segurança no trabalho com inteligência artificial**

</div>
