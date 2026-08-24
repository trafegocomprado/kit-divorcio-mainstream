# Kit Divórcio — PageMind LP

Este diretório contém o pacote estático de produção da landing page do Kit de Ferramentas Pós-Divórcio.

## Atenção antes de usar em tráfego

O build técnico está publicado para validação, mas não deve receber tráfego comercial até substituir os avisos de validação por conteúdo real: garantia, credenciais, três depoimentos, descrição final do mecanismo, acesso vitalício e links legais.

## Preview local

Abra `public/index.html` ou rode:

```bash
npx serve public
```

## Produção

- Repositório: https://github.com/trafegocomprado/kit-divorcio-mainstream
- Cloudflare Pages: https://kit-divorcio-mainstream.pages.dev
- Branch de produção: `main`

## Cloudflare Pages

O projeto usa Direct Upload do diretório `public`, sem etapa de build:

```bash
npm install
npm run deploy
```

O repositório é a fonte versionada. Novos commits precisam de um novo `npm run deploy` porque o projeto Pages não usa Git Integration.

## Estrutura

- `public/` é o artefato que deve ser publicado.
- O build canônico e os relatórios de QA ficam fora deste pacote, em `lp/build/` e `analysis/`.
- Não aponte o Cloudflare para os diretórios de screenshots ou relatórios.

## Checkout e UTMs

Os CTAs apontam para o checkout Hotmart já usado pela página atual. O JavaScript copia parâmetros `utm_*`, `fbclid` e `gclid` da URL da LP para o checkout, preservando `off` e `bid`.
