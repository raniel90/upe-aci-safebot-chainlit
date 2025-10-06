# 🎨 Customização Visual - SafeBot

Guia completo da identidade visual e customização do SafeBot.

---

## 🎯 Identidade Visual

### 🎨 Paleta de Cores

Baseada no SafeBot Legacy (`ui/tailwind.config.ts`):

```css
/* Cores Principais */
--safebot-brand: #FF4017          /* Laranja vibrante (cor principal) */
--safebot-brand-dark: #CC3312     /* Laranja escuro (hover) */
--safebot-brand-light: #FF6B47    /* Laranja claro (destaques) */

/* Fundos */
--safebot-background: #111113     /* Fundo principal (escuro) */
--safebot-background-secondary: #27272A  /* Fundo secundário */

/* Textos */
--safebot-text-primary: #FAFAFA   /* Texto principal (branco) */
--safebot-text-muted: #A1A1AA     /* Texto secundário (cinza) */

/* Estados */
--safebot-positive: #22C55E       /* Verde (sucesso) */
--safebot-destructive: #E53935    /* Vermelho (erro) */
```

### 🛡️ Logo

O SafeBot usa um escudo de proteção com capacete, simbolizando segurança do trabalho:

**Arquivos disponíveis:**
- `public/favicon.ico` - Favicon original do SafeBot Legacy
- `public/logo_dark.svg` - Logo para tema escuro
- `public/logo_light.svg` - Logo para tema claro
- `public/logo.png` - Logo em PNG (se precisar)

**Significado:**
- **Escudo** - Proteção e segurança
- **Capacete** - Equipamento de Proteção Individual (EPI)
- **Cor Laranja (#FF4017)** - Alerta, atenção, segurança

---

## 📁 Arquivos de Customização

### 1. `.chainlit/config.toml`

Configuração principal do Chainlit com tema SafeBot:

```toml
[UI]
name = "🛡️ SafeBot"
description = "Sistema Inteligente de Segurança do Trabalho"
custom_css = "/public/custom.css"

[UI.theme]
default = "dark"

[UI.theme.dark]
background = "#111113"
paper = "#27272A"

[UI.theme.dark.primary]
main = "#FF4017"
dark = "#CC3312"
light = "#FF6B47"
```

### 2. `public/custom.css`

CSS customizado com estilos específicos do SafeBot:
- Cores da marca aplicadas em botões, links, scrollbar
- Animações suaves
- Estilos para roles (supervisor/trabalhador)
- Tema de login personalizado

### 3. `chainlit.md`

Página de boas-vindas exibida antes do login:
- Apresentação do SafeBot
- Explicação dos perfis
- Tecnologias usadas

### 4. `.chainlit/translations/pt-BR.json`

Traduções para português brasileiro:
- Textos da interface
- Mensagens de erro
- Labels de botões

---

## 🎨 Customizações Aplicadas

### ✅ Tema Escuro (Padrão)

```css
Background: #111113 (quase preto)
Cards/Paper: #27272A (cinza escuro)
Primary Color: #FF4017 (laranja SafeBot)
Text: #FAFAFA (branco)
```

### ✅ Tema Claro (Opcional)

```css
Background: #FAFAFA (branco)
Cards/Paper: #F5F5F5 (cinza claro)
Primary Color: #FF4017 (laranja SafeBot)
Text: #18181B (preto)
```

### ✅ Componentes Customizados

- **Botões** - Laranja com gradiente e sombra
- **Links** - Laranja claro (#FF6B47)
- **Scrollbar** - Cor da marca
- **Loading** - Animação pulsante
- **Mensagens** - Borda lateral laranja
- **Inputs** - Borda laranja no foco

### ✅ Tela de Login

Personalização especial para a tela de autenticação:
- Background com gradiente
- Logo com sombra
- Botão com gradiente e elevação
- Efeito hover suave

---

## 🛠️ Como Modificar

### Alterar Cores

Edite `public/custom.css` e `.chainlit/config.toml`:

```css
/* Em custom.css */
:root {
  --safebot-brand: #SUA_COR_AQUI;
  --safebot-brand-dark: #SUA_COR_ESCURA;
  --safebot-brand-light: #SUA_COR_CLARA;
}
```

```toml
# Em config.toml
[UI.theme.dark.primary]
main = "#SUA_COR_AQUI"
dark = "#SUA_COR_ESCURA"
light = "#SUA_COR_CLARA"
```

### Trocar Logo

1. Substitua os arquivos em `public/`:
   - `favicon.ico` - Favicon do navegador
   - `logo_dark.svg` - Logo para tema escuro
   - `logo_light.svg` - Logo para tema claro

2. Mantenha as dimensões recomendadas:
   - **Favicon**: 32x32px ou 64x64px
   - **Logo SVG**: 120x120px (viewBox)

### Adicionar Fontes Customizadas

Em `.chainlit/config.toml`:

```toml
[UI]
custom_font = "https://fonts.googleapis.com/css2?family=SUA_FONTE:wght@400;500;700&display=swap"
```

E em `public/custom.css`:

```css
body {
  font-family: 'SUA_FONTE', sans-serif;
}
```

### Customizar Mensagens

Edite `.chainlit/translations/pt-BR.json`:

```json
{
  "components": {
    "auth": {
      "signin": {
        "title": "Seu Título Customizado"
      }
    }
  }
}
```

---

## 📊 Aplicação das Cores por Contexto

### 🔴 Cor Principal (`#FF4017`) - Quando Usar

- ✅ Botões primários (CTA)
- ✅ Links importantes
- ✅ Ícones de marca
- ✅ Barras de progresso
- ✅ Badges de destaque
- ✅ Bordas de foco

### 🟠 Cor Clara (`#FF6B47`) - Quando Usar

- ✅ Hover em links
- ✅ Destaques secundários
- ✅ Ícones ativos
- ✅ Texto de código
- ✅ Labels importantes

### 🟤 Cor Escura (`#CC3312`) - Quando Usar

- ✅ Hover em botões
- ✅ Sombras coloridas
- ✅ Bordas ativas
- ✅ Estados pressed

### ⚫ Fundos Escuros - Quando Usar

- ✅ Background principal (`#111113`)
- ✅ Cards e containers (`#27272A`)
- ✅ Tooltips
- ✅ Dropdowns

---

## 🎯 Boas Práticas

### ✅ Fazer

- ✅ Usar cores da paleta SafeBot
- ✅ Manter contraste adequado (WCAG AA)
- ✅ Testar em tema claro e escuro
- ✅ Usar animações suaves (0.3s)
- ✅ Documentar mudanças

### ❌ Evitar

- ❌ Cores muito vibrantes fora da paleta
- ❌ Animações muito rápidas (< 0.2s)
- ❌ Textos sem contraste suficiente
- ❌ Logos pixelados ou distorcidos
- ❌ Sobrecarga de efeitos visuais

---

## 🧪 Testar Customizações

### 1. Verificar Tema Escuro

```bash
# Inicie o SafeBot
chainlit run chainlit_app.py

# Acesse: http://localhost:8000
# Verifique:
# - Logo aparece corretamente
# - Cores estão aplicadas
# - Contraste é adequado
```

### 2. Verificar Tema Claro

No navegador:
1. Abra as ferramentas de desenvolvimento (F12)
2. Alterne para tema claro nas configurações do Chainlit
3. Verifique se as cores funcionam bem

### 3. Verificar Responsividade

Teste em diferentes tamanhos de tela:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

---

## 📱 Responsividade

O CSS inclui breakpoints para mobile:

```css
@media (max-width: 768px) {
  .login-logo {
    width: 80px;
    height: 80px;
  }
  
  .card-container {
    margin: 8px;
  }
}
```

---

## 🎨 Exemplos de Uso

### Botão Customizado

```css
.my-button {
  background: linear-gradient(90deg, #FF4017 0%, #FF6B47 100%);
  color: #FAFAFA;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.my-button:hover {
  box-shadow: 0 6px 20px rgba(255, 64, 23, 0.6);
  transform: translateY(-2px);
}
```

### Card com Tema SafeBot

```css
.safebot-card {
  background-color: #27272A;
  border: 1px solid rgba(255, 64, 23, 0.2);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.safebot-card:hover {
  border-color: #FF4017;
  box-shadow: 0 4px 12px rgba(255, 64, 23, 0.3);
}
```

---

## 🔍 Inspeção de Elementos

Para inspecionar e modificar estilos em tempo real:

1. Abra o DevTools (F12)
2. Vá para a aba "Elements"
3. Selecione o elemento
4. Modifique os estilos na aba "Styles"
5. Copie as mudanças para `custom.css`

---

## 📚 Referências

### Documentação

- [Chainlit Customization](https://docs.chainlit.io/customization)
- [Material-UI Theming](https://mui.com/material-ui/customization/theming/)
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

### Ferramentas Úteis

- [Coolors](https://coolors.co/) - Paletas de cores
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) - Teste de contraste
- [SVG Optimizer](https://jakearchibald.github.io/svgomg/) - Otimizar SVGs
- [Favicon Generator](https://realfavicongenerator.net/) - Gerar favicons

---

## 🚀 Deploy em Produção

Ao fazer deploy, certifique-se de:

- ✅ Arquivos `public/` estão incluídos
- ✅ Caminhos dos arquivos estão corretos
- ✅ CSS está minificado (opcional)
- ✅ Imagens estão otimizadas
- ✅ Temas foram testados

---

## 💡 Dicas Avançadas

### Cache Busting

Se as mudanças de CSS não aparecem:

```toml
# Em config.toml
custom_css = "/public/custom.css?v=2"
```

### Debug de Estilos

Adicione ao `custom.css`:

```css
* {
  outline: 1px solid red !important;
}
```

(Remova depois de debugar!)

### Performance

- Use CSS nativo ao invés de JavaScript quando possível
- Minimize animações em dispositivos móveis
- Otimize imagens (use SVG quando possível)
- Use `transform` ao invés de `top/left` para animações

---

**🛡️ SafeBot - Visual profissional para segurança profissional!**
