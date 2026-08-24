# Deployment

- GitHub: https://github.com/trafegocomprado/kit-divorcio-mainstream
- Cloudflare account: `MPX E. D. L.`
- Cloudflare Pages project: `kit-divorcio-mainstream`
- Production URL: https://kit-divorcio-mainstream.pages.dev
- Production branch: `main`
- Build output: `public`
- Method: Direct Upload via Wrangler

## Deploy

```bash
npm install
npm run deploy
```

O projeto Pages não usa Git Integration. Cada atualização no repositório deve ser seguida por um novo deploy do diretório `public`.
