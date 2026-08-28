# Natural PT-BR Copy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar uma versão da landing page que soe escrita originalmente em português brasileiro.

**Architecture:** A página continua estática e autocontida. A alteração fica restrita ao conteúdo textual do HTML; os contratos de vídeo, checkout, acessibilidade e layout são preservados e verificados por testes.

**Tech Stack:** HTML, CSS e JavaScript sem framework; pytest para regressão; Text Editor BR para legibilidade; Wrangler para Cloudflare Pages.

---

### Task 1: Fixar o contrato editorial

**Files:**
- Create: `tests/test_natural_ptbr_copy.py`
- Test: `tests/test_natural_ptbr_copy.py`

- [ ] **Step 1: Escrever o teste de regressão**

O teste deve exigir as novas frases principais, bloquear os calques identificados e confirmar a presença do preço e do checkout.

- [ ] **Step 2: Confirmar a falha no HTML antigo**

Run: `python -m pytest tests/test_natural_ptbr_copy.py -q`

Expected: FAIL porque a nova headline ainda não existe.

### Task 2: Reescrever a copy

**Files:**
- Modify: `public/index.html`
- Modify: `../../lp/build/index.html`
- Modify: `../../lp/build/copy-extracted.txt`
- Modify: `../../lp/deploy/github-cloudflare/index.html`
- Modify: `../../lp/deploy/github-cloudflare/public/index.html`

- [ ] **Step 1: Aplicar a revisão editorial no arquivo canônico**

Preservar atributos, IDs, links e scripts. Trocar apenas o texto visível, a descrição da página e microtextos acessíveis relacionados.

- [ ] **Step 2: Sincronizar os pacotes**

Copiar o HTML canônico para o pacote de deploy e para `public/index.html`; gerar novamente a extração de copy.

- [ ] **Step 3: Rodar a análise de legibilidade**

Run: `python C:/Users/Marcilio/.codex/skills/text-editor-br/scripts/analyze.py --input ../../lp/build/copy-extracted.txt --compare ../../analysis/copy-publicada-2026-08-27.txt --content-type lp --output ../../analysis/text-editor-reescrita-2026-08-28.json`

Expected: melhora de Flesch e redução de frases difíceis, sem novos padrões de IA.

### Task 3: Verificar e publicar

**Files:**
- Test: `tests/test_natural_ptbr_copy.py`
- Test: `tests/test_social_proof.py`
- Test: `tests/test_report_social_proof.py`

- [ ] **Step 1: Rodar todos os testes**

Run: `python -m pytest tests -q`

Expected: PASS.

- [ ] **Step 2: Verificar a página no navegador em desktop e mobile**

Confirmar ausência de overflow, funcionamento do FAQ, dos CTAs e do carregamento dos quatro vídeos.

- [ ] **Step 3: Versionar, publicar e conferir produção**

Fazer commit da revisão, integrar à `main`, enviar ao GitHub e publicar `public` no projeto `kit-divorcio-mainstream`. Comparar o hash do HTML publicado com o arquivo do repositório.
