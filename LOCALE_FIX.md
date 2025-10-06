# 🌍 Fix: Locale pt-BR não carrega

## ✅ Verificações

### 1. Confirmar configuração do config.toml
```toml
[UI]
default_locale = "pt-BR"
```

### 2. Verificar se o arquivo de tradução existe e está correto
```bash
ls -la .chainlit/translations/pt-BR.json
chainlit lint-translations
```

## 🔧 Soluções

### Solução 1: Limpar cache do Chainlit
```bash
rm -rf .chainlit/.files .chainlit/chat_files
```

### Solução 2: Limpar cache do navegador
1. Abra o DevTools (F12)
2. Clique com botão direito no botão de refresh
3. Selecione "Empty Cache and Hard Reload" (Chrome) ou "Hard Refresh" (Firefox)

Ou use:
- Chrome/Edge: `Ctrl+Shift+Delete` (Windows) ou `Cmd+Shift+Delete` (Mac)
- Firefox: `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)

### Solução 3: Modo anônimo/privado
Teste em uma janela anônima para garantir que não há cache:
- Chrome: `Ctrl+Shift+N` (Windows) ou `Cmd+Shift+N` (Mac)
- Firefox: `Ctrl+Shift+P` (Windows) ou `Cmd+Shift+P` (Mac)

### Solução 4: Reiniciar o servidor Chainlit
```bash
# Parar o servidor (Ctrl+C)
# Limpar cache
rm -rf .chainlit/.files

# Reiniciar
chainlit run chainlit_app.py
```

### Solução 5: Verificar no localStorage do navegador
1. Abra DevTools (F12)
2. Vá em "Application" > "Local Storage"
3. Procure por chave relacionada a `locale` ou `language`
4. Delete se existir
5. Recarregue a página

### Solução 6: Verificar configuração de idioma do navegador
O Chainlit pode estar usando o idioma do navegador ao invés do `default_locale`.

**Chrome:**
1. Settings > Languages
2. Adicione "Português (Brasil)" como primeiro idioma

**Firefox:**
1. Settings > Language
2. Adicione "Português [pt-br]" como primeiro idioma

## 🧪 Teste
Depois de aplicar as soluções:

1. Abra uma janela anônima
2. Acesse: http://localhost:8000
3. Verifique se a tela de login mostra:
   - Título: "🛡️ SafeBot - Entrar no Sistema"
   - Campo: "Nome de Usuário" (não "Email address")
   - Botão: "Entrar" (não "Sign In")

## 📝 Debug adicional

Se ainda não funcionar, verifique os logs do navegador:

1. Abra DevTools (F12)
2. Vá em "Console"
3. Procure por erros relacionados a:
   - `i18n`
   - `locale`
   - `translation`
   - `pt-BR`

E compartilhe os erros encontrados.

## ⚠️ Notas Importantes

- **NÃO é necessário JavaScript customizado** - O Chainlit tem i18n nativo
- O arquivo `public/login_text.js` deve estar **comentado** no `config.toml`
- O arquivo `.chainlit/translations/pt-BR.json` deve seguir a estrutura oficial do Chainlit
