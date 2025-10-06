# 🚀 Quick Start - Sistema de Roles

Guia rápido para testar as diferentes experiências do SafeBot por perfil de usuário.

---

## 🎯 Objetivo

O SafeBot adapta completamente sua comunicação baseado no perfil do usuário:
- 👔 **Supervisor** → Linguagem técnica, análises completas
- 👷 **Trabalhador** → Linguagem simples, orientações práticas

---

## ⚡ Teste Rápido (5 minutos)

### 1️⃣ Inicie o SafeBot

```bash
cd safebot-chainlit
poetry shell
chainlit run chainlit_app.py
```

### 2️⃣ Teste o Perfil de TRABALHADOR

**Login:**
- Username: `trabalhador`
- Password: `trabalhador123`

**Faça a pergunta:**
```
"Meu capacete está rachado, o que faço?"
```

**Observe:**
- ✅ Linguagem simples e direta
- ✅ Passo a passo claro
- ✅ Muitos emojis 🛡️ ⚠️ ✅
- ✅ Tom amigável e encorajador
- ✅ Exemplos práticos do dia a dia

### 3️⃣ Teste o Perfil de SUPERVISOR

**Faça logout** (canto superior direito) e faça novo login:

**Login:**
- Username: `supervisor`
- Password: `supervisor123`

**Faça a MESMA pergunta:**
```
"Meu capacete está rachado, o que faço?"
```

**Observe:**
- ✅ Linguagem técnica e formal
- ✅ Fundamentação legal completa
- ✅ Estrutura hierárquica (seções numeradas)
- ✅ Citações de artigos da NR-06
- ✅ Análise de responsabilidades

---

## 🔄 Comparação Lado a Lado

### Mesma Pergunta, Respostas Diferentes!

#### 👷 Trabalhador

```
Opa! Situação seria essa do capacete rachado! ⚠️
Vou te explicar direitinho o que fazer:

## 🛑 PARE AGORA!

Se seu capacete está rachado, PARE de trabalhar com ele!
Um capacete rachado NÃO protege. É perigoso!

## ✅ O que fazer AGORA:

1. Pare de usar o capacete rachado
2. Avise seu supervisor/chefe IMEDIATAMENTE
3. Peça um capacete novo na hora
4. A empresa tem que dar de graça!

💡 É seu DIREITO ter equipamento em bom estado.
NUNCA trabalhe com EPI quebrado ou danificado!

Precisa de mais ajuda? É só perguntar! 👷🛡️
```

#### 👔 Supervisor

```
**PROCEDIMENTO PARA SUBSTITUIÇÃO DE EPI DANIFICADO**

**1. FUNDAMENTAÇÃO LEGAL**

Conforme item 6.6.1, alínea "e" da NR-06:
"Compete ao empregador substituir imediatamente quando 
danificado ou extraviado."

**2. PROCEDIMENTO IMEDIATO**

a) Avaliação do dano:
   - Classificar gravidade (trinca superficial vs. rachadura estrutural)
   - Determinar causa (impacto, desgaste, defeito de fabricação)
   
b) Ações imediatas:
   - Retirar de uso o EPI danificado
   - Fornecer substituto imediato ao trabalhador
   - Registrar ocorrência em FE-EPI

**3. DOCUMENTAÇÃO**

Registros obrigatórios:
- Ficha de Entrega de novo EPI (data, CA, assinatura)
- Investigação se dano resultou de não conformidade
- Atualização de inventário de estoque

**4. ANÁLISE DE CAUSA RAIZ**

Investigar:
- EPI estava dentro da vida útil?
- Uso correto pelo trabalhador?
- Armazenamento adequado?
- Necessidade de treinamento adicional

**5. RESPONSABILIDADES**

Empregador (NR-06, 6.6.1.e):
✅ Substituição imediata e gratuita

Empregado (NR-06, 6.7.1.c):
✅ Comunicar qualquer alteração que o torne impróprio

**Prazo:** IMEDIATO (não pode haver trabalho sem EPI adequado)
```

---

## 📋 Perguntas Sugeridas para Teste

### Para TRABALHADOR (user)

```
1. "Quais EPIs eu preciso para soldar?"
2. "Como limpar minha máscara de proteção?"
3. "A empresa pode me cobrar pelos EPIs?"
4. "Meu protetor auricular incomoda, posso tirar?"
5. "Como sei se meu EPI está vencido?"
```

### Para SUPERVISOR (supervisor)

```
1. "Elabore um checklist de auditoria de conformidade NR-06"
2. "Quais são as responsabilidades legais do empregador no fornecimento de EPIs?"
3. "Como estruturar um POP para controle de entrega de EPIs?"
4. "Análise técnica: trabalhador sofreu acidente sem usar protetor auricular"
5. "Que documentação é obrigatória para comprovar conformidade com NR-06?"
```

---

## 👥 Todos os Usuários de Teste

| Username | Senha | Role | Quando usar |
|----------|-------|------|-------------|
| `trabalhador` | `trabalhador123` | user | Teste de linguagem simples |
| `operador1` | `operador123` | user | Outro exemplo de trabalhador |
| `supervisor` | `supervisor123` | supervisor | Teste de linguagem técnica |
| `tecnico_seguranca` | `tecnico123` | supervisor | Outro exemplo de gestor |

---

## 🎓 O Que Observar

### Diferenças no Prompt Engineering

#### 👷 Trabalhador
- Começa com empatia: "Opa!", "Que bom que você perguntou!"
- Usa **MAIÚSCULAS** para ênfase
- Analogias do dia a dia
- Passo a passo numerado simples
- Muitos emojis
- Perguntas finais: "Entendeu?", "Precisa de mais ajuda?"

#### 👔 Supervisor
- Começa com título técnico: "**PROCEDIMENTO PARA...**"
- Seções numeradas e hierárquicas
- Subseções com letras (a, b, c)
- Citações completas: "item 6.6.1, alínea 'e' da NR-06"
- Checklists e frameworks
- Análise de responsabilidades
- Considerações de implementação

---

## 🔍 Teste Avançado

### Experimento: Mesma Pergunta, Usuários Diferentes

Faça logout e login alternando entre perfis, sempre fazendo a mesma pergunta:

**Pergunta:**
```
"Como fazer uma auditoria de conformidade de EPIs?"
```

**Resultado esperado:**

- 👷 **Trabalhador:** "Auditoria? Isso é trabalho do pessoal da segurança! Mas vou te explicar o que eles fazem e como você pode ajudar..."

- 👔 **Supervisor:** "**ESTRUTURA DE AUDITORIA DE CONFORMIDADE NR-06**\n\n**1. PLANEJAMENTO**\n- Definir escopo\n- Selecionar amostra..."

---

## ⚙️ Customização

### Adicionar Seus Próprios Usuários

1. **Edite `auth.py`:**
```python
"seu_usuario": {
    "password": os.getenv("SAFEBOT_SEU_PASSWORD", "senha123"),
    "metadata": {
        "role": "user",  # ou "supervisor"
        "name": "Seu Nome",
        "provider": "credentials"
    }
}
```

2. **Adicione ao `.env`:**
```env
SAFEBOT_SEU_PASSWORD=sua-senha-segura
```

3. **Reinicie o SafeBot**

---

## 🐛 Troubleshooting

### Não vejo diferença nas respostas

**Solução:**
1. Verifique se está fazendo **logout** antes de trocar de usuário
2. Confirme o username e role no topo da tela
3. Limpe o cache do navegador (Ctrl+Shift+R)
4. Reinicie o servidor Chainlit

### Login não funciona

**Solução:**
1. Verifique se as senhas no `.env` estão corretas
2. Confirme que o arquivo `auth.py` foi atualizado
3. Reinicie o servidor após mudanças no `.env`

### Prompts não mudaram

**Solução:**
1. Verifique se o arquivo `prompts.py` existe
2. Confirme que `chainlit_app.py` está importando de `prompts.py`
3. Reinicie o servidor

---

## 📚 Próximos Passos

Após testar:

1. 📖 Leia [`ROLES.md`](ROLES.md) - Documentação completa das roles
2. 🔐 Leia [`AUTHENTICATION.md`](AUTHENTICATION.md) - Configuração de autenticação
3. 🎯 Experimente criar uma nova role customizada
4. 🔧 Ajuste os prompts em `prompts.py` conforme sua necessidade

---

## 💡 Dicas Finais

### Para Demonstrações

1. **Abra duas janelas do navegador** (modo anônimo em uma)
2. Faça login com perfis diferentes em cada janela
3. Faça a mesma pergunta nos dois
4. Compare as respostas lado a lado!

### Para Desenvolvimento

1. **Ative o verbose no `.chainlit/config.toml`:**
```toml
[project]
verbose = true
```

2. **Monitore os logs no terminal** para ver o prompt completo sendo enviado

---

**🎭 SafeBot - Experimente a diferença!**
