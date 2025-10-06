# 🐧 Guia de Instalação - Ubuntu 25.04

Este guia fornece instruções passo a passo para instalar e executar o **SafeBot Chainlit** em sistemas Ubuntu 25.04 (ou versões superiores).

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação do Python 3.12+](#instalação-do-python-312)
3. [Instalação do Poetry](#instalação-do-poetry)
4. [Clonagem do Projeto](#clonagem-do-projeto)
5. [Configuração do Ambiente](#configuração-do-ambiente)
6. [Instalação das Dependências](#instalação-das-dependências)
7. [Configuração das Variáveis de Ambiente](#configuração-das-variáveis-de-ambiente)
8. [Execução do SafeBot](#execução-do-safebot)
9. [Solução de Problemas](#solução-de-problemas)

---

## 🔧 Pré-requisitos

Antes de começar, certifique-se de que seu sistema está atualizado:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🐍 Instalação do Python 3.12+

### Verificar versão do Python

Primeiro, verifique se o Python 3.12+ já está instalado:

```bash
python3 --version
```

Se a versão for **3.12 ou superior**, pule para a [próxima seção](#instalação-do-poetry).

### Instalar Python 3.12 (se necessário)

Se você não tiver Python 3.12+, instale usando o PPA deadsnakes:

```bash
# Adicionar o repositório PPA do deadsnakes
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Instalar Python 3.12 e ferramentas essenciais
sudo apt install python3.12 python3.12-venv python3.12-dev python3-pip -y

# Verificar a instalação
python3.12 --version
```

### Configurar Python 3.12 como padrão (opcional)

```bash
# Criar um alias permanente no seu .bashrc
echo "alias python3=python3.12" >> ~/.bashrc
source ~/.bashrc

# Verificar
python3 --version
```

---

## 📦 Instalação do Poetry

O Poetry é o gerenciador de dependências utilizado neste projeto.

### Método 1: Instalação via instalador oficial (recomendado)

```bash
# Instalar Poetry usando o instalador oficial
curl -sSL https://install.python-poetry.org | python3 -

# Adicionar Poetry ao PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verificar instalação
poetry --version
```

### Método 2: Instalação via pip (alternativa)

```bash
pip3 install poetry

# Adicionar ao PATH se necessário
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verificar instalação
poetry --version
```

### Configurar Poetry (opcional)

```bash
# Criar ambientes virtuais dentro do projeto (recomendado)
poetry config virtualenvs.in-project true

# Verificar configuração
poetry config --list
```

---

## 📥 Clonagem do Projeto

Clone o repositório do GitHub:

```bash
# Navegar para o diretório onde deseja clonar o projeto
cd ~

# Clonar o repositório
git clone https://github.com/raniel90/upe-aci-safebot-chainlit.git

# Entrar no diretório do projeto
cd upe-aci-safebot-chainlit
```

---

## 🔐 Configuração do Ambiente

### Obter sua chave da OpenAI

Você precisa de uma chave de API da OpenAI. Se ainda não tiver:

1. Acesse: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave gerada (comece com `sk-...`)

⚠️ **Importante**: Guarde sua chave em um local seguro! Ela não será exibida novamente.

---

## 📦 Instalação das Dependências

Agora vamos instalar todas as dependências do projeto usando Poetry:

```bash
# Certificar-se de estar no diretório do projeto
cd ~/upe-aci-safebot-chainlit

# Instalar as dependências (pode levar alguns minutos)
poetry install

# Se houver erro com Python 3.12, especifique a versão:
poetry env use python3.12
poetry install
```

**Saída esperada:**
```
Installing dependencies from lock file

Package operations: 45 installs, 0 updates, 0 removals

  • Installing ...
  ...
  • Installing chainlit (1.x.x)
  
Writing lock file
```

---

## ⚙️ Configuração das Variáveis de Ambiente

### Criar arquivo `.env`

```bash
# Copiar o arquivo de exemplo
cp .env.example .env

# Editar o arquivo .env com seu editor preferido
nano .env
# Ou use: vim .env, gedit .env, code .env, etc.
```

### Configurar as variáveis

No arquivo `.env`, adicione sua chave da OpenAI e configure as senhas:

```env
# ============================================================================
# OPENAI API (OBRIGATÓRIO)
# ============================================================================
OPENAI_API_KEY=sk-sua-chave-da-openai-aqui

# ============================================================================
# AUTENTICAÇÃO (OBRIGATÓRIO - Altere as senhas padrão!)
# ============================================================================
# Senhas para os diferentes perfis de usuário
SAFEBOT_SUPERVISOR_PASSWORD=sua-senha-supervisor-segura
SAFEBOT_USER_PASSWORD=sua-senha-trabalhador-segura
SAFEBOT_OPERADOR1_PASSWORD=sua-senha-operador-segura
SAFEBOT_TECNICO_PASSWORD=sua-senha-tecnico-segura

# Secret para autenticação do Chainlit (gere uma string aleatória longa)
CHAINLIT_AUTH_SECRET=seu-secret-muito-seguro-e-aleatorio-aqui
```

### Gerar um secret seguro (opcional)

Para gerar um `CHAINLIT_AUTH_SECRET` seguro:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copie a saída e cole no arquivo `.env`.

### Salvar e sair

- **Nano**: `Ctrl + O` (salvar), `Enter`, `Ctrl + X` (sair)
- **Vim**: `Esc`, `:wq`, `Enter`

---

## 🚀 Execução do SafeBot

### Método 1: Ativar ambiente virtual e executar

```bash
# Ativar o ambiente virtual do Poetry
poetry shell

# Executar o SafeBot
chainlit run chainlit_app.py
```

### Método 2: Executar diretamente com Poetry (sem ativar shell)

```bash
# Executar diretamente
poetry run chainlit run chainlit_app.py
```

### Acesso à interface

Após executar, você verá algo como:

```
2024-10-06 - Loaded .env file
2024-10-06 - Your app is available at http://localhost:8000
2024-10-06 - Playground is available at http://localhost:8000/playground
```

**Abra seu navegador** e acesse:

```
http://localhost:8000
```

### Fazer login

Na primeira vez, você verá uma tela de login. Use um dos perfis disponíveis:

**👷 Trabalhador (Linguagem Simples):**
- **Usuário**: `trabalhador`
- **Senha**: A senha que você definiu em `SAFEBOT_USER_PASSWORD`

**👔 Supervisor (Linguagem Técnica):**
- **Usuário**: `supervisor`
- **Senha**: A senha que você definiu em `SAFEBOT_SUPERVISOR_PASSWORD`

---

## 🎯 Testando o SafeBot

Após fazer login, teste com perguntas como:

```
🔹 Quais EPIs são obrigatórios para trabalho em altura?
🔹 Como fazer uma auditoria de conformidade de EPIs?
🔹 Qual a responsabilidade do empregador segundo a NR-06?
```

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'chainlit'"

**Causa**: Dependências não foram instaladas corretamente.

**Solução**:
```bash
poetry install
```

---

### Erro: "OPENAI_API_KEY not found"

**Causa**: Arquivo `.env` não foi criado ou a chave não foi configurada.

**Solução**:
```bash
# Verificar se o arquivo .env existe
ls -la .env

# Se não existir, criar a partir do exemplo
cp .env.example .env

# Editar e adicionar sua chave
nano .env
```

---

### Erro: "Python version not supported"

**Causa**: Versão do Python é inferior a 3.12.

**Solução**:
```bash
# Verificar versão instalada
python3 --version

# Se for inferior a 3.12, instale o Python 3.12
sudo apt install python3.12 python3.12-venv -y

# Configure o Poetry para usar Python 3.12
poetry env use python3.12
poetry install
```

---

### Erro: "Port 8000 already in use"

**Causa**: Outra aplicação está usando a porta 8000.

**Solução 1: Parar a aplicação que está usando a porta**
```bash
# Descobrir qual processo está usando a porta 8000
sudo lsof -i :8000

# Matar o processo (substitua PID pelo número do processo)
kill -9 PID
```

**Solução 2: Usar outra porta**
```bash
chainlit run chainlit_app.py --port 8080
```

---

### Erro: "PDF da NR-06 não encontrado"

**Causa**: O arquivo PDF não está no diretório correto.

**Solução**:
```bash
# Verificar se o arquivo existe
ls -lh data/pdfs/nr-06-atualizada-2022-1.pdf

# Se não existir, você precisa obter o PDF da NR-06
# e colocá-lo em: data/pdfs/nr-06-atualizada-2022-1.pdf
```

---

### Erro de permissão ao instalar Poetry ou pacotes

**Causa**: Permissões insuficientes.

**Solução**:
```bash
# NÃO use sudo com Poetry!
# Em vez disso, certifique-se de que seu usuário tem permissões

# Se necessário, ajuste as permissões do diretório .local
mkdir -p ~/.local/bin
chmod -R u+rwx ~/.local
```

---

### ChromaDB/SQLite errors

**Causa**: Dependências de sistema faltando.

**Solução**:
```bash
sudo apt install build-essential libsqlite3-dev -y
poetry install
```

---

## 📚 Recursos Adicionais

- **Documentação completa**: [README.md](README.md)
- **Guia de autenticação**: [AUTHENTICATION.md](AUTHENTICATION.md)
- **Sistema de perfis**: [ROLES.md](ROLES.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)

---

## 🆘 Precisa de Ajuda?

Se você encontrar problemas não listados aqui:

1. Verifique o arquivo [README.md](README.md) para mais informações
2. Consulte a documentação do [Chainlit](https://docs.chainlit.io)
3. Abra uma issue no GitHub do projeto

---

## 🔄 Atualizando o Projeto

Para atualizar o SafeBot com as últimas mudanças do repositório:

```bash
# Navegar até o diretório do projeto
cd ~/upe-aci-safebot-chainlit

# Baixar as últimas mudanças
git pull origin main

# Atualizar dependências
poetry install

# Reiniciar o aplicativo
poetry run chainlit run chainlit_app.py
```

---

## 🎉 Pronto!

Agora você tem o **SafeBot** rodando no seu Ubuntu! 

**🛡️ Aproveite e trabalhe com segurança!**

[⬆ Voltar ao topo](#-guia-de-instalação---ubuntu-2504)
