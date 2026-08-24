# YouTube Social Proof Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preservar os quatro depoimentos em vídeo da página original na LP publicada e corrigir o relatório M1+M2+M3 e seu PDF para reconhecer essa prova existente.

**Architecture:** A LP continuará estática. Cada vídeo será um card com thumbnail WebP local e um botão que cria um iframe `youtube-nocookie.com` somente após o clique; um link direto permanece como fallback. O gerador do relatório passará a declarar a prova existente sem alterar retroativamente o score original, regenerando HTML contínuo, HTML paginado e PDF.

**Tech Stack:** HTML/CSS/JavaScript sem framework, Python stdlib para testes estruturais, Node.js para o gerador de relatório, Wrangler 4 para Cloudflare Pages, GitHub CLI e PyMuPDF para inspeção do PDF.

---

## Mapa de arquivos

- Criar `tests/test_social_proof.py`: contrato TDD da LP e dos quatro assets.
- Criar `tests/test_report_social_proof.py`: contrato factual do gerador e dos HTMLs do relatório.
- Modificar `outputs/kit-divorcio/lp/build/index.html`: cards, estilos e carregador sob demanda.
- Criar `outputs/kit-divorcio/lp/build/assets/proof/*.webp`: thumbnails locais.
- Modificar `outputs/kit-divorcio/lp/build/copy-extracted.txt`: texto puro da LP corrigida.
- Modificar `outputs/kit-divorcio/lp/build/build.json`: inventário de prova e gates atualizados.
- Sincronizar `public/` em `outputs/kit-divorcio/lp/deploy/github-cloudflare/` e neste repositório.
- Modificar `outputs/kit-divorcio/reports/generate_report.mjs`: M1, M2 e M3 factualmente corrigidos.
- Regenerar os dois HTMLs e `pagemind_kit-divorcio_m1m2m3_report.pdf`.
- Modificar `outputs/kit-divorcio/EXECUTION_LOG.md` e `FINAL_VERIFICATION.md` com o novo commit/deployment.

### Task 1: Criar o teste de regressão da LP

**Files:**
- Create: `tests/test_social_proof.py`
- Test: `tests/test_social_proof.py`

- [ ] **Step 1: Escrever o teste que exige quatro vídeos e zero placeholder de depoimento**

```python
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = Path(os.environ.get("LANDING_INDEX", ROOT / "public" / "index.html"))
IDS = ("NjGfd9zKDf4", "KLxQ5Dr6W8s", "XrZHAOsWbcs", "__rkMASEkDc")
ASSETS = tuple(f"assets/proof/depoimento-{n}.webp" for n in range(1, 5))

html = INDEX.read_text(encoding="utf-8")

assert all(html.count(video_id) >= 2 for video_id in IDS)
assert html.count('class="video-proof__trigger"') == 4
assert html.count('data-youtube-id="') == 4
assert "youtube-nocookie.com/embed/" in html
assert "[VALIDAÇÃO PENDENTE] Depoimento real" not in html
assert "<iframe" not in html.casefold()
assert all((INDEX.parent / asset).is_file() for asset in ASSETS)
assert all(f"https://www.youtube.com/watch?v={video_id}" in html for video_id in IDS)
print("PASS: quatro vídeos reais, assets locais e carregamento sob demanda")
```

- [ ] **Step 2: Executar e comprovar RED**

Run:

```powershell
python tests\test_social_proof.py
```

Expected: `FAIL`/`AssertionError`, porque o HTML atual contém zero IDs e três placeholders.

- [ ] **Step 3: Commitar somente o teste vermelho**

```powershell
git add tests/test_social_proof.py
git commit -m "test: require original YouTube social proof"
```

### Task 2: Baixar e validar as thumbnails originais

**Files:**
- Create: `outputs/kit-divorcio/lp/build/assets/proof/depoimento-1.webp`
- Create: `outputs/kit-divorcio/lp/build/assets/proof/depoimento-2.webp`
- Create: `outputs/kit-divorcio/lp/build/assets/proof/depoimento-3.webp`
- Create: `outputs/kit-divorcio/lp/build/assets/proof/depoimento-4.webp`

- [ ] **Step 1: Baixar as quatro imagens com mapeamento fixo**

```powershell
$dest = "outputs\kit-divorcio\lp\build\assets\proof"
New-Item -ItemType Directory -Path $dest -Force | Out-Null
$sources = @(
  'https://sirlenevilela.com.br/wp-content/uploads/2026/08/WhatsApp-Image-2026-08-21-at-22.06.09-3.webp',
  'https://sirlenevilela.com.br/wp-content/uploads/2026/08/WhatsApp-Image-2026-08-21-at-22.06.08.webp',
  'https://sirlenevilela.com.br/wp-content/uploads/2026/08/WhatsApp-Image-2026-08-21-at-22.06.09.webp',
  'https://sirlenevilela.com.br/wp-content/uploads/2026/08/WhatsApp-Image-2026-08-21-at-22.06.09-1.webp'
)
for ($i = 0; $i -lt $sources.Count; $i++) {
  Invoke-WebRequest -Uri $sources[$i] -OutFile (Join-Path $dest "depoimento-$($i + 1).webp")
}
```

- [ ] **Step 2: Validar assinatura WebP e tamanho não vazio**

```powershell
Get-ChildItem $dest -File | ForEach-Object {
  $bytes = [IO.File]::ReadAllBytes($_.FullName)
  if ($bytes.Length -lt 1000 -or [Text.Encoding]::ASCII.GetString($bytes, 0, 4) -ne 'RIFF' -or [Text.Encoding]::ASCII.GetString($bytes, 8, 4) -ne 'WEBP') {
    throw "Asset WebP inválido: $($_.FullName)"
  }
}
```

### Task 3: Implementar os cards e o player sob demanda

**Files:**
- Modify: `outputs/kit-divorcio/lp/build/index.html:318-325`
- Modify: `outputs/kit-divorcio/lp/build/index.html:607-630`
- Modify: `outputs/kit-divorcio/lp/build/index.html:737-780`

- [ ] **Step 1: Trocar os estilos de placeholder por grid e card de vídeo**

```css
.proof-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; margin-top:var(--space-5); }
.video-proof { overflow:hidden; border:1px solid rgba(255,250,242,.22); border-radius:var(--radius-md); background:rgba(255,255,255,.035); }
.video-proof__media { position:relative; aspect-ratio:16/9; background:#071d18; }
.video-proof__trigger { position:absolute; inset:0; width:100%; min-height:44px; padding:0; border:0; cursor:pointer; background:transparent; }
.video-proof__trigger img { width:100%; height:100%; object-fit:cover; }
.video-proof__trigger::after { content:'▶'; position:absolute; inset:50% auto auto 50%; display:grid; width:4rem; height:4rem; place-items:center; border-radius:50%; color:var(--surface); background:var(--coral); transform:translate(-50%,-50%); }
.video-proof__player { width:100%; height:100%; border:0; }
.video-proof__body { padding:1rem 1.1rem 1.2rem; }
.video-proof__body p { margin:0; color:#d6e0dc; }
.video-proof__body a { display:inline-flex; min-height:44px; align-items:center; margin-top:.55rem; color:#f0ad9b; }
.sr-only { position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }
@media (max-width:760px) { .proof-grid { grid-template-columns:1fr; } }
```

- [ ] **Step 2: Substituir os três placeholders pelos quatro cards**

Cada card seguirá exatamente este contrato, variando número, ID e asset:

```html
<article class="video-proof" data-reveal>
  <div class="video-proof__media">
    <button class="video-proof__trigger" type="button" data-youtube-id="NjGfd9zKDf4" aria-label="Reproduzir depoimento 1">
      <img src="assets/proof/depoimento-1.webp" width="640" height="360" loading="lazy" decoding="async" alt="Thumbnail do depoimento em vídeo 1">
    </button>
    <span class="sr-only video-proof__status" aria-live="polite"></span>
  </div>
  <div class="video-proof__body">
    <p>Relato em vídeo · metodologia Cura Energética aplicada ao Divórcio Energético</p>
    <a href="https://www.youtube.com/watch?v=NjGfd9zKDf4" target="_blank" rel="noopener noreferrer">Abrir no YouTube</a>
  </div>
</article>
```

- [ ] **Step 3: Adicionar allowlist e ativação do iframe**

```js
const allowedVideoIds = new Set(['NjGfd9zKDf4', 'KLxQ5Dr6W8s', 'XrZHAOsWbcs', '__rkMASEkDc']);
document.querySelectorAll('.video-proof__trigger').forEach((button, index) => {
  button.addEventListener('click', () => {
    const videoId = button.dataset.youtubeId;
    if (!allowedVideoIds.has(videoId)) return;
    const iframe = document.createElement('iframe');
    iframe.className = 'video-proof__player';
    iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0`;
    iframe.title = `Depoimento em vídeo ${index + 1}`;
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    const status = button.parentElement.querySelector('.video-proof__status');
    button.replaceWith(iframe);
    if (status) status.textContent = `Player do depoimento ${index + 1} carregado`;
  });
});
```

- [ ] **Step 4: Sincronizar o HTML e os assets para o pacote e o repositório**

```powershell
Copy-Item "outputs\kit-divorcio\lp\build\index.html" "outputs\kit-divorcio\lp\deploy\github-cloudflare\public\index.html" -Force
Copy-Item "outputs\kit-divorcio\lp\build\index.html" "outputs\kit-divorcio\repository\kit-divorcio-mainstream\public\index.html" -Force
Copy-Item "outputs\kit-divorcio\lp\build\assets\proof" "outputs\kit-divorcio\lp\deploy\github-cloudflare\public\assets" -Recurse -Force
Copy-Item "outputs\kit-divorcio\lp\build\assets\proof" "outputs\kit-divorcio\repository\kit-divorcio-mainstream\public\assets" -Recurse -Force
```

- [ ] **Step 5: Executar GREEN e regressão estrutural**

```powershell
python tests\test_social_proof.py
python "..\..\lp\build\tests\validate_landing.py"
```

Expected: os dois comandos imprimem `PASS`.

- [ ] **Step 6: Commitar a LP e os assets**

```powershell
git add public/index.html public/assets/proof
git commit -m "feat: restore YouTube social proof videos"
```

### Task 4: Criar o teste factual do relatório

**Files:**
- Create: `tests/test_report_social_proof.py`
- Test: `tests/test_report_social_proof.py`

- [ ] **Step 1: Escrever o teste RED do gerador e dos outputs**

```python
import os
from pathlib import Path

report_dir = Path(os.environ["REPORT_DIR"])
generator = (report_dir / "generate_report.mjs").read_text(encoding="utf-8")
ids = ("NjGfd9zKDf4", "KLxQ5Dr6W8s", "XrZHAOsWbcs", "__rkMASEkDc")

assert "4 depoimentos em vídeo" in generator
assert "prova existente, pouco contextualizada" in generator
assert "quatro cards de vídeo" in generator
assert "a prova existe; ainda precisa de contexto textual autorizado" in generator
assert "a prova ainda precisa ser real" not in generator
assert all(video_id in generator for video_id in ids)
print("PASS: gerador M1 M2 M3 reconhece os quatro vídeos")
```

- [ ] **Step 2: Executar e comprovar RED**

```powershell
$env:REPORT_DIR="D:\OpenAI-Codex\PageMind Skills\outputs\kit-divorcio\reports"
python tests\test_report_social_proof.py
```

Expected: `AssertionError` em `4 depoimentos em vídeo`.

- [ ] **Step 3: Commitar o teste vermelho**

```powershell
git add tests/test_report_social_proof.py
git commit -m "test: require report to recognize video proof"
```

### Task 5: Corrigir M1, M2 e M3 no gerador

**Files:**
- Modify: `outputs/kit-divorcio/reports/generate_report.mjs:14-45`
- Modify: `outputs/kit-divorcio/reports/generate_report.mjs:95-151`

- [ ] **Step 1: Adicionar inventário estático da prova**

```js
const proofVideos = [
  ['01', 'NjGfd9zKDf4'],
  ['02', 'KLxQ5Dr6W8s'],
  ['03', 'XrZHAOsWbcs'],
  ['04', '__rkMASEkDc'],
];
```

- [ ] **Step 2: Corrigir o M1 sem alterar o score retroativamente**

Adicionar um card `Inventário de prova` com `4 depoimentos em vídeo` e os quatro IDs. Manter `Prova social 4 → 7` e `Matriz de prova 7/31`, explicando: `prova existente, pouco contextualizada e usada cedo demais`.

- [ ] **Step 3: Corrigir o M2**

Alterar a decisão de ecossistema para:

```html
<div class="pending avoid"><strong>Decisão de ecossistema</strong><br>Não adicionar order bump, upsell ou downsell nesta rodada. Primeiro validar mensagem, contexto dos quatro vídeos existentes e garantia.</div>
```

- [ ] **Step 4: Corrigir o M3 e os P0**

Registrar `quatro cards de vídeo com carregamento sob demanda`, remover a exigência de novos depoimentos e usar:

```html
<div class="pending avoid"><strong>Publicação comercial bloqueada</strong><br>A prova existe; ainda precisa de contexto textual autorizado. Validar garantia, credenciais, síntese dos vídeos, mecanismo, acesso vitalício e URLs legais.</div>
```

- [ ] **Step 5: Regenerar os dois HTMLs e executar GREEN**

```powershell
node "outputs\kit-divorcio\reports\generate_report.mjs"
$env:REPORT_DIR="D:\OpenAI-Codex\PageMind Skills\outputs\kit-divorcio\reports"
python "outputs\kit-divorcio\repository\kit-divorcio-mainstream\tests\test_report_social_proof.py"
```

Expected: `PASS: gerador M1 M2 M3 reconhece os quatro vídeos`.

### Task 6: Regenerar e inspecionar o PDF

**Files:**
- Modify: `outputs/kit-divorcio/reports/pagemind_kit-divorcio_m1m2m3_report.html`
- Modify: `outputs/kit-divorcio/reports/pagemind_kit-divorcio_m1m2m3_report_paginated.html`
- Modify: `outputs/kit-divorcio/reports/pagemind_kit-divorcio_m1m2m3_report.pdf`
- Modify: `outputs/kit-divorcio/reports/pdf_inspection.json`

- [ ] **Step 1: Gerar o PDF com a skill oficial**

```powershell
python "$env:USERPROFILE\.codex\skills\lp-report-pdf\scripts\html_to_pdf.py" `
  --input "outputs\kit-divorcio\reports\pagemind_kit-divorcio_m1m2m3_report_paginated.html" `
  --output "outputs\kit-divorcio\reports\pagemind_kit-divorcio_m1m2m3_report.pdf"
```

- [ ] **Step 2: Rasterizar e validar métricas**

```powershell
python "outputs\kit-divorcio\reports\inspect_pdf.py"
```

Expected: `all_pages_have_text: true` e `blocks_outside_page: 0`.

- [ ] **Step 3: Inspecionar visualmente todas as páginas PNG**

Abrir `outputs/kit-divorcio/tmp/pdfs/kit-divorcio/page-*.png` e rejeitar cards cortados, páginas órfãs, imagens vazias ou sobreposição.

### Task 7: Gates de browser e atualização dos artefatos

**Files:**
- Modify: `outputs/kit-divorcio/lp/build/build.json`
- Modify: `outputs/kit-divorcio/lp/build/copy-extracted.txt`
- Modify: `outputs/kit-divorcio/analysis/design_review_kit-divorcio.md`
- Modify: `outputs/kit-divorcio/analysis/qa_kit-divorcio.md`

- [ ] **Step 1: Extrair novamente a copy e confirmar anti-IA**

Remover tags do HTML, colapsar whitespace e salvar `copy-extracted.txt`; executar a verificação existente e confirmar score ≥ 75.

- [ ] **Step 2: Testar a LP local em 1280×800, 768×1024, 390×844 e 375×667**

Em cada viewport verificar overflow horizontal, alvos visíveis ≥44 px e headings sem viúva. No desktop e mobile, clicar no primeiro card e confirmar exatamente um iframe `youtube-nocookie.com/embed/NjGfd9zKDf4`.

- [ ] **Step 3: Atualizar `build.json`**

Adicionar `social_proof.youtube_videos = 4`, os quatro IDs, `lazy_loaded = true`, `local_thumbnails = true` e registrar novamente os gates executados.

### Task 8: Commit, push, deploy e verificação de produção

**Files:**
- Modify: `README.md`
- Modify: `package-manifest.json`
- Modify: `outputs/kit-divorcio/EXECUTION_LOG.md`
- Modify: `outputs/kit-divorcio/FINAL_VERIFICATION.md`

- [ ] **Step 1: Executar a suíte final antes do commit**

```powershell
python tests\test_social_proof.py
$env:REPORT_DIR="D:\OpenAI-Codex\PageMind Skills\outputs\kit-divorcio\reports"
python tests\test_report_social_proof.py
python "..\..\lp\build\tests\validate_landing.py"
git diff --check
```

Expected: três `PASS`, zero erro de whitespace.

- [ ] **Step 2: Commitar e enviar**

```powershell
git add --all
git commit -m "feat: publish video social proof and correct report"
git push origin main
```

- [ ] **Step 3: Fazer deploy do commit final**

```powershell
$commit=(git rev-parse HEAD).Trim()
wrangler pages deploy public --project-name kit-divorcio-mainstream --branch main --commit-hash $commit --commit-message "feat: publish video social proof and correct report"
```

- [ ] **Step 4: Verificar produção**

Confirmar HTTP 200, hash remoto igual ao `public/index.html`, quatro IDs, quatro thumbnails 200, zero iframe no DOM inicial e um iframe após clique. Confirmar `git ls-remote origin refs/heads/main` igual ao commit local e deployment Production associado à mesma origem.

- [ ] **Step 5: Registrar evidências finais**

Atualizar `EXECUTION_LOG.md` e `FINAL_VERIFICATION.md` com commit, deployment ID, URL de produção, resultados dos testes, páginas do PDF e a observação factual: `a prova existe e foi preservada; contexto textual permanece P0`.
