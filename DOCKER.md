# 🐳 Guia Docker - SafeBot Chainlit

Este guia explica como executar o **SafeBot Chainlit** usando Docker e Docker Compose.

---

## 📋 Índice

1. [Por que usar Docker?](#por-que-usar-docker)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação do Docker](#instalação-do-docker)
4. [Configuração](#configuração)
5. [Executar com Docker Compose (Recomendado)](#executar-com-docker-compose-recomendado)
6. [Executar com Docker (Manual)](#executar-com-docker-manual)
7. [Comandos Úteis](#comandos-úteis)
8. [Volumes e Persistência](#volumes-e-persistência)
9. [Solução de Problemas](#solução-de-problemas)
10. [Deploy em Produção](#deploy-em-produção)

---

## 🎯 Por que usar Docker?

**Vantagens:**

✅ **Instalação Simplificada** - Não precisa instalar Python, Poetry ou dependências  
✅ **Ambiente Isolado** - Não conflita com outras instalações Python  
✅ **Portabilidade** - Funciona em qualquer sistema (Linux, macOS, Windows)  
✅ **Reprodutibilidade** - Mesmo ambiente em dev e produção  
✅ **Fácil Deploy** - Pronto para cloud (AWS, Azure, GCP, etc.)  
✅ **Segurança** - Executa com usuário não-root

---

## 📋 Pré-requisitos

### Sistema Operacional

- ✅ Linux (Ubuntu, Debian, CentOS, etc.)
- ✅ macOS (Intel ou Apple Silicon)
- ✅ Windows 10/11 com WSL2

### Requisitos de Software

- **Docker** 20.10 ou superior
- **Docker Compose** 2.0 ou superior (geralmente incluído no Docker Desktop)

### Chave da OpenAI

Você precisará de uma chave de API da OpenAI. Se ainda não tiver:

1. Acesse: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Faça login ou crie uma conta
3. Clique em "Create new secret key"
4. Copie a chave gerada (começa com `sk-...`)

---

## 🔧 Instalação do Docker

### Ubuntu/Debian

```bash
# Atualizar pacotes
sudo apt update

# Instalar dependências
sudo apt install -y ca-certificates curl gnupg lsb-release

# Adicionar chave GPG oficial do Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Adicionar repositório Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Adicionar seu usuário ao grupo docker (evita usar sudo)
sudo usermod -aG docker $USER

# Aplicar mudanças (ou faça logout/login)
newgrp docker

# Verificar instalação
docker --version
docker compose version
```

### macOS

**Opção 1: Docker Desktop (Recomendado)**

1. Baixe: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Instale o arquivo `.dmg`
3. Abra o Docker Desktop
4. Aguarde inicialização

**Opção 2: Homebrew**

```bash
brew install --cask docker
```

### Windows

1. Instale o WSL2: [https://docs.microsoft.com/windows/wsl/install](https://docs.microsoft.com/windows/wsl/install)
2. Baixe Docker Desktop: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
3. Instale e reinicie o computador
4. Abra Docker Desktop e aguarde inicialização

---

## ⚙️ Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/raniel90/upe-aci-safebot-chainlit.git
cd upe-aci-safebot-chainlit
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com seu editor preferido
nano .env
# Ou: vim .env, code .env, gedit .env, etc.
```

**Configure no arquivo `.env`:**

```env
# ============================================================================
# OPENAI API (OBRIGATÓRIO)
# ============================================================================
OPENAI_API_KEY=sk-sua-chave-da-openai-aqui

# ============================================================================
# AUTENTICAÇÃO (Altere as senhas!)
# ============================================================================
SAFEBOT_SUPERVISOR_PASSWORD=sua-senha-supervisor-segura
SAFEBOT_USER_PASSWORD=sua-senha-trabalhador-segura
SAFEBOT_OPERADOR1_PASSWORD=sua-senha-operador-segura
SAFEBOT_TECNICO_PASSWORD=sua-senha-tecnico-segura

# Secret para autenticação (gere uma string aleatória longa)
CHAINLIT_AUTH_SECRET=seu-secret-muito-seguro-e-aleatorio-aqui
```

**Gerar um secret seguro:**

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 🚀 Executar com Docker Compose (Recomendado)

Docker Compose é a forma mais simples de executar o SafeBot.

### Iniciar o SafeBot

```bash
# Build e iniciar (primeira vez ou após mudanças)
docker compose up --build

# Ou em modo detached (background)
docker compose up -d
```

### Acessar a Interface

Abra seu navegador em:

```
http://localhost:8000
```

### Ver Logs

```bash
# Logs em tempo real
docker compose logs -f

# Últimas 100 linhas
docker compose logs --tail=100
```

### Parar o SafeBot

```bash
# Parar containers
docker compose stop

# Parar e remover containers
docker compose down

# Parar, remover containers E volumes (⚠️ apaga dados)
docker compose down -v
```

---

## 🐳 Executar com Docker (Manual)

Se preferir usar Docker diretamente sem Compose:

### Build da Imagem

```bash
docker build -t safebot-chainlit:latest .
```

### Executar Container

```bash
docker run -d \
  --name safebot-chainlit \
  -p 8000:8000 \
  -e OPENAI_API_KEY="sk-sua-chave-aqui" \
  -e SAFEBOT_SUPERVISOR_PASSWORD="supervisor123" \
  -e SAFEBOT_USER_PASSWORD="trabalhador123" \
  -e CHAINLIT_AUTH_SECRET="seu-secret-aqui" \
  -v safebot_chromadb:/app/tmp/chromadb \
  --restart unless-stopped \
  safebot-chainlit:latest
```

### Ver Logs

```bash
docker logs -f safebot-chainlit
```

### Parar Container

```bash
docker stop safebot-chainlit
docker rm safebot-chainlit
```

---

## 📦 Comandos Úteis

### Docker Compose

```bash
# Ver status dos containers
docker compose ps

# Reiniciar serviços
docker compose restart

# Rebuild sem cache
docker compose build --no-cache

# Ver uso de recursos
docker compose stats

# Executar comandos dentro do container
docker compose exec safebot bash

# Ver versão do Chainlit dentro do container
docker compose exec safebot chainlit --version
```

### Docker

```bash
# Listar containers ativos
docker ps

# Listar todas as imagens
docker images

# Remover imagens não utilizadas
docker image prune -a

# Limpar tudo (⚠️ cuidado!)
docker system prune -a --volumes

# Inspecionar container
docker inspect safebot-chainlit

# Ver uso de recursos
docker stats safebot-chainlit
```

---

## 💾 Volumes e Persistência

O Docker Compose cria volumes nomeados para persistir dados:

### Volumes Criados

```yaml
chromadb_data:   # Banco de dados vetorial (embeddings da NR-06)
chainlit_data:   # Configurações e histórico do Chainlit
```

### Comandos para Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect upe-aci-safebot-chainlit_chromadb_data

# Fazer backup de um volume
docker run --rm \
  -v upe-aci-safebot-chainlit_chromadb_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/chromadb-backup.tar.gz -C /data .

# Restaurar backup
docker run --rm \
  -v upe-aci-safebot-chainlit_chromadb_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/chromadb-backup.tar.gz -C /data
```

### Usar PDFs Customizados

Descomente no `docker-compose.yml`:

```yaml
volumes:
  - ./data/pdfs:/app/data/pdfs:ro
```

Então coloque seus PDFs em `./data/pdfs/`.

---

## 🔧 Solução de Problemas

### Container não inicia

**Verificar logs:**
```bash
docker compose logs safebot
```

**Causas comuns:**
- ❌ `OPENAI_API_KEY` não configurada
- ❌ Porta 8000 já em uso
- ❌ Arquivo `.env` não existe

### Porta 8000 já em uso

**Opção 1: Parar o processo que usa a porta**
```bash
# Linux/Mac
sudo lsof -i :8000
sudo kill -9 <PID>

# Windows (PowerShell)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Opção 2: Usar outra porta**

Edite `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Usa porta 8080 no host
```

### Erro de permissão em volumes

```bash
# Remover volumes e recriar
docker compose down -v
docker compose up -d
```

### Container reinicia constantemente

```bash
# Ver logs detalhados
docker compose logs --tail=50 safebot

# Verificar healthcheck
docker inspect safebot-chainlit | grep -A 10 Health
```

### Imagem muito grande

O Dockerfile usa multi-stage build para otimização, mas se precisar reduzir mais:

```bash
# Ver tamanho da imagem
docker images safebot-chainlit

# Remover dependências não usadas no Dockerfile
# e rebuild com:
docker compose build --no-cache
```

### Atualizar após mudanças no código

```bash
# Rebuild e reiniciar
docker compose up -d --build

# Ou forçar recreação
docker compose up -d --force-recreate --build
```

---

## 🌐 Deploy em Produção

### Considerações de Segurança

1. **Mudar senhas padrão** no `.env`
2. **Usar HTTPS** (reverse proxy com Nginx/Traefik)
3. **Limitar recursos** (CPU/memória no docker-compose.yml)
4. **Habilitar firewall** (apenas porta HTTPS pública)
5. **Backups regulares** dos volumes

### Exemplo com Nginx Reverse Proxy

Crie `nginx.conf`:

```nginx
server {
    listen 80;
    server_name safebot.seudominio.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Deploy em Cloud

**AWS ECS/Fargate:**
```bash
# Build para registry
docker tag safebot-chainlit:latest YOUR_ECR_REPO/safebot:latest
docker push YOUR_ECR_REPO/safebot:latest
```

**Google Cloud Run:**
```bash
gcloud run deploy safebot \
  --image safebot-chainlit:latest \
  --platform managed \
  --port 8000 \
  --set-env-vars OPENAI_API_KEY=sk-...
```

**Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name safebot \
  --image safebot-chainlit:latest \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=sk-...
```

---

## 📊 Monitoramento

### Logs estruturados

O container usa logging JSON. Integre com:

- **ELK Stack** (Elasticsearch + Logstash + Kibana)
- **Grafana Loki**
- **CloudWatch** (AWS)
- **Stackdriver** (GCP)

### Métricas

```bash
# Ver uso de recursos em tempo real
docker stats safebot-chainlit

# Exportar para Prometheus (adicione exporter)
```

---

## 🆘 Precisa de Ajuda?

- 📚 [Documentação Docker](https://docs.docker.com)
- 🐳 [Docker Compose Reference](https://docs.docker.com/compose/)
- 📖 [README Principal](README.md)
- 🔐 [Guia de Autenticação](AUTHENTICATION.md)

---

## 🎉 Pronto!

Agora você tem o **SafeBot** rodando em container Docker! 

**🛡️ Docker: Deploy simples, ambiente consistente!**

[⬆ Voltar ao topo](#-guia-docker---safebot-chainlit)
