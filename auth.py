"""
Módulo de Autenticação do SafeBot
Implementa autenticação por senha e preparado para OAuth
"""

import os
from typing import Optional, Dict
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

# Usuários do sistema (em produção, use um banco de dados!)
USERS_DB = {
    # SUPERVISOR - Gestor de Segurança do Trabalho
    "supervisor": {
        "password": os.getenv("SAFEBOT_SUPERVISOR_PASSWORD", "supervisor123"),
        "metadata": {
            "role": "supervisor",
            "name": "Gestor de Segurança",
            "provider": "credentials",
            "description": "Profissional de gestão em segurança do trabalho"
        }
    },
    
    # USER - Trabalhador de Chão de Fábrica
    "trabalhador": {
        "password": os.getenv("SAFEBOT_USER_PASSWORD", "trabalhador123"),
        "metadata": {
            "role": "user",
            "name": "Trabalhador",
            "provider": "credentials",
            "description": "Profissional operacional"
        }
    },
    
    # Exemplos adicionais de usuários
    "operador1": {
        "password": os.getenv("SAFEBOT_OPERADOR1_PASSWORD", "operador123"),
        "metadata": {
            "role": "user",
            "name": "Operador de Máquinas",
            "provider": "credentials",
            "description": "Operador de máquinas"
        }
    },
    
    "tecnico_seguranca": {
        "password": os.getenv("SAFEBOT_TECNICO_PASSWORD", "tecnico123"),
        "metadata": {
            "role": "supervisor",
            "name": "Técnico de Segurança",
            "provider": "credentials",
            "description": "Técnico em segurança do trabalho"
        }
    },
}

# ============================================================================
# AUTENTICAÇÃO POR SENHA
# ============================================================================

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Callback de autenticação por senha
    
    Args:
        username: Nome de usuário
        password: Senha
        
    Returns:
        cl.User se autenticado com sucesso, None caso contrário
    """
    # Verificar se usuário existe
    user_data = USERS_DB.get(username)
    
    if not user_data:
        # Usuário não encontrado
        return None
    
    # Verificar senha
    if user_data["password"] != password:
        # Senha incorreta
        return None
    
    # Autenticação bem-sucedida!
    return cl.User(
        identifier=username,
        metadata=user_data["metadata"]
    )


# ============================================================================
# OAUTH (DESABILITADO - Descomente para habilitar)
# ============================================================================

# NOTA: Para usar OAuth, descomente o código abaixo e configure as variáveis
# de ambiente correspondentes no .env (OAUTH_GITHUB_CLIENT_ID, etc.)

# @cl.oauth_callback
# def oauth_callback(
#     provider_id: str,
#     token: str,
#     raw_user_data: Dict[str, str],
#     default_user: cl.User,
# ) -> Optional[cl.User]:
#     """
#     Callback de autenticação OAuth
#     
#     Atualmente preparado para:
#     - GitHub
#     - Google
#     - Azure AD
#     
#     Para habilitar, configure as variáveis de ambiente no .env:
#     - OAUTH_GITHUB_CLIENT_ID e OAUTH_GITHUB_CLIENT_SECRET
#     - OAUTH_GOOGLE_CLIENT_ID e OAUTH_GOOGLE_CLIENT_SECRET
#     - etc.
#     
#     Args:
#         provider_id: Identificador do provedor OAuth
#         token: Token de acesso
#         raw_user_data: Dados brutos do usuário do provedor
#         default_user: Objeto de usuário padrão do Chainlit
#         
#     Returns:
#         cl.User customizado ou None para negar acesso
#     """
#     
#     # Customizar dados do usuário baseado no provedor
#     if provider_id == "google":
#         # Exemplo: Restringir acesso a domínio específico
#         # Descomente para usar:
#         # allowed_domain = os.getenv("ALLOWED_GOOGLE_DOMAIN", "example.org")
#         # if raw_user_data.get("hd") != allowed_domain:
#         #     return None
#         
#         # Adicionar informações adicionais
#         default_user.metadata["email"] = raw_user_data.get("email")
#         default_user.metadata["picture"] = raw_user_data.get("picture")
#         default_user.metadata["provider"] = "google"
#         
#     elif provider_id == "github":
#         # Customizar para GitHub
#         default_user.metadata["email"] = raw_user_data.get("email")
#         default_user.metadata["avatar_url"] = raw_user_data.get("avatar_url")
#         default_user.metadata["provider"] = "github"
#         
#     elif provider_id == "azure":
#         # Customizar para Azure AD
#         default_user.metadata["email"] = raw_user_data.get("email")
#         default_user.metadata["provider"] = "azure"
#     
#     # Adicionar role padrão se não existir
#     if "role" not in default_user.metadata:
#         default_user.metadata["role"] = "user"
#     
#     return default_user


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_user_from_session() -> Optional[cl.User]:
    """
    Recupera o usuário da sessão atual
    
    Returns:
        cl.User ou None se não autenticado
    """
    return cl.user_session.get("user")


def is_supervisor(user: cl.User) -> bool:
    """
    Verifica se o usuário é supervisor/gestor de segurança
    
    Args:
        user: Objeto de usuário
        
    Returns:
        True se for supervisor, False caso contrário
    """
    return user.metadata.get("role") == "supervisor"


def is_user(user: cl.User) -> bool:
    """
    Verifica se o usuário é trabalhador operacional
    
    Args:
        user: Objeto de usuário
        
    Returns:
        True se for user, False caso contrário
    """
    return user.metadata.get("role") == "user"


def get_user_role(user: cl.User) -> str:
    """
    Obtém a role do usuário
    
    Args:
        user: Objeto de usuário
        
    Returns:
        Role do usuário (supervisor, user, etc.)
    """
    return user.metadata.get("role", "user")


def get_user_name(user: cl.User) -> str:
    """
    Obtém o nome de exibição do usuário
    
    Args:
        user: Objeto de usuário
        
    Returns:
        Nome de exibição ou identifier como fallback
    """
    return user.metadata.get("name", user.identifier)


# ============================================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================================

def validate_user_access(user: cl.User, resource: str) -> bool:
    """
    Valida se o usuário tem acesso a um recurso específico
    
    Args:
        user: Objeto de usuário
        resource: Nome do recurso
        
    Returns:
        True se tem acesso, False caso contrário
    """
    # Supervisores têm acesso completo
    if is_supervisor(user):
        return True
    
    # Recursos específicos para supervisores
    supervisor_only_resources = [
        "audit_reports",
        "compliance_analysis",
        "procedure_generation",
        "team_management"
    ]
    
    if resource in supervisor_only_resources and not is_supervisor(user):
        return False
    
    # Usuários operacionais têm acesso básico
    return True


# ============================================================================
# LOGOUT
# ============================================================================

@cl.on_logout
def on_logout(request, response):
    """
    Callback executado quando usuário faz logout
    
    Use para limpar cookies, sessões, etc.
    """
    # Exemplo: limpar cookie customizado
    # response.delete_cookie("my_custom_cookie")
    pass
