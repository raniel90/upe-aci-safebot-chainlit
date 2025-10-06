# 🤝 Guia de Contribuição - SafeBot

Obrigado por considerar contribuir com o SafeBot! Este documento fornece diretrizes para contribuir com o projeto.

---

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Melhorias](#sugerir-melhorias)
- [Desenvolvimento](#desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Processo de Review](#processo-de-review)

---

## 🚀 Como Contribuir

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/safebot-chainlit.git
cd safebot-chainlit
```

### 2. Configure o Ambiente

```bash
# Instale dependências
poetry install

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais
```

### 3. Crie uma Branch

```bash
# Sempre crie uma branch para suas mudanças
git checkout -b feature/minha-feature
# ou
git checkout -b bugfix/correcao-bug
```

### 4. Faça suas Alterações

- Siga os [padrões de código](#padrões-de-código)
- Adicione testes se aplicável
- Atualize documentação se necessário

### 5. Commit e Push

```bash
# Commits descritivos
git add .
git commit -m "feat: adiciona funcionalidade X"
git push origin feature/minha-feature
```

### 6. Abra um Pull Request

- Descreva claramente suas mudanças
- Referencie issues relacionadas
- Aguarde review

---

## 🐛 Reportar Bugs

### Antes de Reportar

- ✅ Verifique se o bug já foi reportado
- ✅ Teste na última versão
- ✅ Verifique se é realmente um bug

### Template de Bug Report

```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Como Reproduzir**
Passos para reproduzir:
1. Vá para '...'
2. Faça '...'
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
 - OS: [e.g. macOS 14.0]
 - Python: [e.g. 3.12]
 - Versão: [e.g. 0.1.0]

**Logs de Erro**
```
Cole aqui os logs relevantes
```
```

---

## 💡 Sugerir Melhorias

### Template de Feature Request

```markdown
**Problema Relacionado**
Descrição clara do problema que a feature resolve.

**Solução Proposta**
Descrição da solução que você gostaria.

**Alternativas Consideradas**
Outras soluções que você considerou.

**Contexto Adicional**
Qualquer outro contexto sobre a feature.
```

---

## 🛠️ Desenvolvimento

### Setup Inicial

```bash
# Instalar dependências de desenvolvimento
poetry install --with dev

# Ativar ambiente virtual
poetry shell

# Executar aplicação
chainlit run chainlit_app.py -w
```

### Estrutura de Branches

- `main` - Branch principal (produção)
- `develop` - Branch de desenvolvimento
- `feature/*` - Novas funcionalidades
- `bugfix/*` - Correções de bugs
- `docs/*` - Melhorias na documentação
- `refactor/*` - Refatorações de código

### Testes

```bash
# Executar testes
poetry run pytest

# Com cobertura
poetry run pytest --cov=.

# Testes específicos
poetry run pytest tests/test_rag.py
```

---

## 📝 Padrões de Código

### Python Style Guide

Seguimos o **PEP 8** com algumas adaptações:

```bash
# Formatação automática
poetry run black .

# Linting
poetry run flake8 .

# Type checking (opcional)
poetry run mypy .
```

### Convenções

#### Nomes de Variáveis
```python
# ✅ Bom
user_message = "Hello"
retrieval_chain = ConversationalRetrievalChain(...)
is_valid = True

# ❌ Evite
msg = "Hello"
rc = ConversationalRetrievalChain(...)
valid = True
```

#### Docstrings
```python
def process_message(message: str, context: dict) -> str:
    """
    Processa uma mensagem do usuário com contexto.
    
    Args:
        message: Mensagem do usuário
        context: Contexto da conversa
        
    Returns:
        Resposta processada pelo modelo
        
    Raises:
        ValueError: Se mensagem estiver vazia
    """
    pass
```

#### Imports
```python
# Ordem de imports:
# 1. Standard library
import os
from typing import List

# 2. Third-party
import chainlit as cl
from langchain.chains import ConversationalRetrievalChain

# 3. Local
from .utils import load_pdf
from .config import OPENAI_API_KEY
```

### Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Tipos de commit
feat:     # Nova funcionalidade
fix:      # Correção de bug
docs:     # Apenas documentação
style:    # Formatação, sem mudança de lógica
refactor: # Refatoração de código
test:     # Adicionar/modificar testes
chore:    # Tarefas de manutenção

# Exemplos
git commit -m "feat: adiciona suporte a múltiplas NRs"
git commit -m "fix: corrige bug na busca vetorial"
git commit -m "docs: atualiza README com novos exemplos"
git commit -m "refactor: melhora organização do código RAG"
```

---

## 🔍 Processo de Review

### Checklist do Autor

Antes de submeter um PR, verifique:

- [ ] Código segue os padrões de estilo
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Commits são descritivos
- [ ] Branch está atualizada com `main`
- [ ] Sem conflitos de merge
- [ ] Aplicação funciona localmente

### Checklist do Reviewer

Ao revisar um PR, verifique:

- [ ] Código é legível e bem documentado
- [ ] Não introduz bugs ou quebras
- [ ] Testes cobrem os casos importantes
- [ ] Performance não foi degradada
- [ ] Segurança não foi comprometida
- [ ] Mudanças são consistentes com a arquitetura

### Tipos de Review

- ✅ **Approved** - PR pronto para merge
- 🔄 **Changes Requested** - Requer alterações
- 💬 **Comment** - Sugestões não-bloqueantes

---

## 📚 Áreas para Contribuir

### 🐛 Bugs Conhecidos

Veja issues com label `bug`

### 🌟 Features Desejadas

Veja issues com label `enhancement`

### 📖 Documentação

- Melhorar exemplos
- Adicionar tutoriais
- Traduzir documentação
- Criar videos/GIFs

### 🧪 Testes

- Aumentar cobertura de testes
- Adicionar testes de integração
- Testes de performance

### 🎨 UI/UX

- Melhorar interface Chainlit
- Adicionar temas customizados
- Melhorar formatação de respostas

---

## 🎓 Recursos Úteis

### Documentação Técnica

- [Chainlit Docs](https://docs.chainlit.io)
- [LangChain Docs](https://python.langchain.com)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

### Leitura Recomendada

- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Python Best Practices](https://docs.python-guide.org/)

---

## 💬 Canais de Comunicação

### GitHub Issues

Use para:
- Reportar bugs
- Sugerir features
- Discutir melhorias técnicas

### Discussions

Use para:
- Perguntas gerais
- Ideias e brainstorming
- Compartilhar experiências

---

## 🏆 Reconhecimento

Contribuidores serão:
- Listados no README
- Mencionados nas release notes
- Reconhecidos publicamente

---

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT do projeto.

---

**🛡️ Obrigado por contribuir com o SafeBot!**

Sua contribuição ajuda a tornar ambientes de trabalho mais seguros! 💪
