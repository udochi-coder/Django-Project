# Northstar Student Portal

## Local development

```bash
npm install
npm run dev
```

Set `VITE_API_URL` to the deployed Django service URL to use the live API. Without it, the app opens in demo mode so the interface can be reviewed independently.

## Cloudflare Pages

- Build command: `npm run build`
- Build output directory: `dist`
- Root directory: `frontend`
- Environment variable: `VITE_API_URL=https://<your-render-service>.onrender.com`

The backend login currently expects `email` and `password`. The frontend stores the returned JWT access token and sends it as a Bearer token for result requests.