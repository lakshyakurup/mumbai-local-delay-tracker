# Deployment & Production Architecture

## Deployment Strategy
The application is structured for cloud-native deployment with decoupled frontend and backend services:
- **Frontend:** Deployed on **Vercel** with automatic preview deployments on every pull request.
- **Backend & Data Pipeline:** Hosted on **Render** / **Railway** running Python FastAPI workers and background scheduler tasks.
- **Database:** Managed PostgreSQL instance with automated daily backups.

## Environment Variables
Ensure the following environment variables are configured in your production dashboard (Vercel / Render):
- `DATABASE_URL`: Connection string for the persistent SQL database.
- `NEXT_PUBLIC_API_BASE_URL`: Production backend URL pointing to FastAPI.
- `SECRET_KEY`: Cryptographic signing key for API authentication.
