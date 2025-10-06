# ⚡ Guia Rápido - SafeBot

## 🎯 Escolha seu método (3-5 minutos)

### 🐳 Opção 1: Docker (Mais Fácil - Recomendado)

```bash
# 1. Clonar o repositório
git clone https://github.com/raniel90/upe-aci-safebot-chainlit.git
cd upe-aci-safebot-chainlit

# 2. Configurar variáveis
cp .env.example .env
nano .env  # Adicione sua OPENAI_API_KEY

# 3. Executar com Docker Compose
docker compose up -d

# Pronto! Acesse http://localhost:8000
```

📖 **Guia completo:** [DOCKER.md](DOCKER.md)

---

### 💻 Opção 2: Instalação Manual (Python + Poetry)

#### 1️⃣ Instalar Dependências

```bash
# Instalar Poetry (se não tiver)
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências do projeto
poetry install
```

### 2️⃣ Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar e adicionar sua chave da OpenAI
nano .env
```

Adicione no arquivo `.env`:
```
OPENAI_API_KEY=sk-sua-chave-aqui
```

### 3️⃣ Executar o SafeBot

```bash
# Ativar ambiente virtual
poetry shell

# Iniciar o chat
chainlit run chainlit_app.py
```

O chat abrirá automaticamente em `http://localhost:8000` 🎉

---

## 📝 Comandos Úteis

```bash
# Executar com auto-reload (desenvolvimento)
chainlit run chainlit_app.py -w

# Executar em porta diferente
chainlit run chainlit_app.py --port 8080

# Executar sem abrir o navegador
chainlit run chainlit_app.py -h
```

---

## 🎯 Primeiros Passos no Chat

1. **Aguarde** o carregamento da base de conhecimento (primeira vez leva ~30s)
2. **Faça sua primeira pergunta**, por exemplo:
   - "Quais EPIs são necessários para solda?"
   - "O que diz a NR-06 sobre responsabilidades do empregador?"
3. **Explore as fontes** citadas no painel lateral
4. **Continue a conversa** - o bot lembra do contexto!

---

## 🔧 Troubleshooting

### ❌ Erro: "OPENAI_API_KEY not found"
**Solução:** Verifique se o arquivo `.env` existe e contém sua chave da OpenAI.

### ❌ Erro: "PDF not found"
**Solução:** Verifique se o arquivo `data/pdfs/nr-06-atualizada-2022-1.pdf` existe.

### ❌ Erro: "Port already in use"
**Solução:** Use uma porta diferente com `--port 8080`.

### ❌ Erro ao instalar dependências
**Solução:** 
```bash
# Limpar cache do Poetry
poetry cache clear pypi --all

# Reinstalar
poetry install
```

---

## 📚 Mais Informações

- **README completo**: [README.md](README.md)
- **Guia Docker**: [DOCKER.md](DOCKER.md)
- **Guia Ubuntu**: [INSTALL_UBUNTU.md](INSTALL_UBUNTU.md)
- **Autenticação**: [AUTHENTICATION.md](AUTHENTICATION.md)
- **Documentação Chainlit**: https://docs.chainlit.io

---

**🛡️ Pronto para começar? Execute `chainlit run chainlit_app.py` e boa conversa!**
