# 🔐 Guia de Autenticação - SafeBot

Este documento descreve como configurar e usar a autenticação no SafeBot.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Autenticação por Senha](#autenticação-por-senha)
- [OAuth (Opcional)](#oauth-opcional)
- [Gerenciamento de Usuários](#gerenciamento-de-usuários)
- [Segurança](#segurança)

---

## 🎯 Visão Geral

O SafeBot suporta múltiplos métodos de autenticação:

### ✅ Implementado
- **Autenticação por Senha** - Login com usuário e senha

### 🔧 Preparado (Opcional)
- **OAuth GitHub** - Login com conta GitHub
- **OAuth Google** - Login com conta Google
- **OAuth Azure AD** - Login com conta Microsoft

---

## 🔑 Autenticação por Senha

### Configuração Inicial

1. **Configure as senhas no arquivo `.env`:**

```bash
# Copie o exemplo se ainda não fez
cp .env.example .env

# Edite o arquivo .env
nano .env
```

2. **Defina senhas seguras:**

```env
# IMPORTANTE: Mude estas senhas em produção!
SAFEBOT_ADMIN_PASSWORD=sua-senha-admin-segura
SAFEBOT_USER_PASSWORD=sua-senha-usuario-segura
```

### Usuários Padrão

O sistema vem com dois usuários pré-configurados:

| Usuário | Senha (padrão) | Papel | Descrição |
|---------|----------------|-------|-----------|
| `admin` | `admin123` | Administrador | Acesso completo ao sistema |
| `usuario` | `usuario123` | Usuário | Acesso padrão |

⚠️ **IMPORTANTE**: Altere estas senhas antes de usar em produção!

### Login

1. Acesse o SafeBot: `http://localhost:8000`
2. Será exibida uma tela de login
3. Digite usuário e senha
4. Clique em "Entrar"

![Login Screen](https://via.placeholder.com/600x300?text=Tela+de+Login)

---

## 🌐 OAuth (Opcional)

### GitHub OAuth

#### 1. Criar OAuth App no GitHub

1. Acesse: https://github.com/settings/developers
2. Clique em "New OAuth App"
3. Preencha:
   - **Application name**: SafeBot
   - **Homepage URL**: `http://localhost:8000`
   - **Authorization callback URL**: `http://localhost:8000/auth/oauth/github/callback`
4. Copie o **Client ID** e **Client Secret**

#### 2. Configurar no SafeBot

```bash
# Adicione ao .env
OAUTH_GITHUB_CLIENT_ID=seu_client_id_aqui
OAUTH_GITHUB_CLIENT_SECRET=seu_client_secret_aqui
```

#### 3. Reiniciar o SafeBot

```bash
chainlit run chainlit_app.py
```

Agora aparecerá um botão "Login com GitHub" na tela de login! 🎉

---

### Google OAuth

#### 1. Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com
2. Crie um novo projeto
3. Vá para "APIs & Services" > "Credentials"
4. Clique em "Create Credentials" > "OAuth client ID"
5. Configure:
   - **Application type**: Web application
   - **Authorized redirect URIs**: `http://localhost:8000/auth/oauth/google/callback`
6. Copie o **Client ID** e **Client Secret**

#### 2. Configurar no SafeBot

```bash
# Adicione ao .env
OAUTH_GOOGLE_CLIENT_ID=seu_client_id_aqui
OAUTH_GOOGLE_CLIENT_SECRET=seu_client_secret_aqui

# Opcional: Restringir a domínio específico
ALLOWED_GOOGLE_DOMAIN=example.org
```

#### 3. Reiniciar o SafeBot

```bash
chainlit run chainlit_app.py
```

---

### Azure AD OAuth

#### 1. Registrar Aplicação no Azure AD

1. Acesse: https://portal.azure.com
2. Vá para "Azure Active Directory" > "App registrations"
3. Clique em "New registration"
4. Configure:
   - **Name**: SafeBot
   - **Redirect URI**: `http://localhost:8000/auth/oauth/azure/callback`
5. Copie:
   - **Application (client) ID**
   - **Directory (tenant) ID**
6. Crie um **Client Secret** em "Certificates & secrets"

#### 2. Configurar no SafeBot

```bash
# Adicione ao .env
OAUTH_AZURE_AD_CLIENT_ID=seu_client_id_aqui
OAUTH_AZURE_AD_CLIENT_SECRET=seu_client_secret_aqui
OAUTH_AZURE_AD_TENANT_ID=seu_tenant_id_aqui
```

---

## 👥 Gerenciamento de Usuários

### Adicionar Novo Usuário

Edite o arquivo `auth.py`:

```python
USERS_DB = {
    "admin": {
        "password": os.getenv("SAFEBOT_ADMIN_PASSWORD", "admin123"),
        "metadata": {
            "role": "admin",
            "name": "Administrador",
            "provider": "credentials"
        }
    },
    # ADICIONE NOVO USUÁRIO AQUI
    "joao": {
        "password": os.getenv("SAFEBOT_JOAO_PASSWORD", "senha123"),
        "metadata": {
            "role": "user",
            "name": "João Silva",
            "provider": "credentials"
        }
    },
}
```

E adicione a senha no `.env`:

```env
SAFEBOT_JOAO_PASSWORD=senha-segura-do-joao
```

### Papéis de Usuário

O sistema suporta dois papéis:

#### 👑 Admin (`role: "admin"`)
- Acesso completo ao sistema
- Pode gerenciar usuários (futuro)
- Pode acessar estatísticas (futuro)

#### 👤 User (`role: "user"`)
- Acesso padrão ao chat
- Pode fazer consultas
- Histórico de conversas próprio

### Customizar Permissões

Edite a função `validate_user_access` em `auth.py`:

```python
def validate_user_access(user: cl.User, resource: str) -> bool:
    """
    Valida se o usuário tem acesso a um recurso específico
    """
    # Admins têm acesso a tudo
    if is_admin(user):
        return True
    
    # Adicione lógica customizada
    if resource == "advanced_features":
        # Apenas admins podem acessar features avançadas
        return False
    
    return True
```

---

## 🔒 Segurança

### Boas Práticas

#### ✅ Senhas Fortes

```bash
# Use senhas com pelo menos 12 caracteres
# Combine letras, números e símbolos
SAFEBOT_ADMIN_PASSWORD=S3nh@F0rt3#2024!
```

#### ✅ Variáveis de Ambiente

```bash
# NUNCA comite o arquivo .env no Git
# Ele já está no .gitignore

# Em produção, use serviços de secrets:
# - AWS Secrets Manager
# - Azure Key Vault
# - HashiCorp Vault
```

#### ✅ HTTPS em Produção

```bash
# Configure um proxy reverso (Nginx/Caddy)
# com certificado SSL

# Exemplo com Caddy:
# Caddyfile
your-domain.com {
    reverse_proxy localhost:8000
}
```

#### ✅ Rate Limiting

```toml
# Adicione ao .chainlit/config.toml
[features]
rate_limiting = true
max_requests_per_minute = 60
```

### Hashing de Senhas

⚠️ **Importante**: O código atual usa comparação direta de senhas para simplicidade. Em produção, use hashing:

```python
import bcrypt

# Ao criar usuário
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Ao verificar
bcrypt.checkpw(password.encode(), hashed)
```

### Integração com Banco de Dados

Para produção, substitua o dicionário `USERS_DB` por consultas ao banco:

```python
import sqlite3

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT password_hash, metadata FROM users WHERE username = ?",
        (username,)
    )
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return None
    
    password_hash, metadata = result
    
    if bcrypt.checkpw(password.encode(), password_hash):
        return cl.User(identifier=username, metadata=metadata)
    
    return None
```

---

## 🧪 Testando Autenticação

### Teste Local

1. **Inicie o SafeBot:**
```bash
chainlit run chainlit_app.py
```

2. **Teste login com usuário padrão:**
- Usuário: `admin`
- Senha: `admin123` (ou a que você configurou)

3. **Verifique a sessão:**
- O nome do usuário deve aparecer na mensagem de boas-vindas
- A sessão deve persistir durante toda a conversa

### Teste de Logout

1. Clique no botão de logout no canto superior direito
2. Você deve ser redirecionado para a tela de login
3. Faça login novamente para confirmar

---

## 🔧 Troubleshooting

### ❌ Erro: "Authentication callback not found"

**Solução**: Verifique se o arquivo `auth.py` está no mesmo diretório que `chainlit_app.py`.

### ❌ Erro: "Invalid credentials"

**Solução**:
1. Verifique se as senhas no `.env` estão corretas
2. Confirme que o usuário existe no `USERS_DB`
3. Verifique se não há espaços extras nas variáveis

### ❌ OAuth não aparece

**Solução**:
1. Confirme que as variáveis `OAUTH_*` estão configuradas no `.env`
2. Reinicie o SafeBot após adicionar as configurações
3. Verifique os logs para erros de configuração

### ❌ Sessão expira rapidamente

**Solução**: Ajuste o timeout no `.chainlit/config.toml`:

```toml
[project]
# Tempo em segundos (3600 = 1 hora)
session_timeout = 3600

# Tempo de expiração da sessão do usuário (15 dias)
user_session_timeout = 1296000
```

---

## 📚 Recursos Adicionais

### Documentação Chainlit
- [Authentication Overview](https://docs.chainlit.io/authentication/overview)
- [Password Authentication](https://docs.chainlit.io/authentication/password)
- [OAuth Providers](https://docs.chainlit.io/authentication/oauth)

### Segurança
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

## 🎯 Próximos Passos

- [ ] Implementar hashing de senhas com bcrypt
- [ ] Integrar com banco de dados
- [ ] Adicionar recuperação de senha
- [ ] Implementar 2FA (autenticação de dois fatores)
- [ ] Adicionar logs de auditoria
- [ ] Implementar rate limiting por usuário

---

**🛡️ SafeBot - Segurança não é só no trabalho, é também no sistema!**
