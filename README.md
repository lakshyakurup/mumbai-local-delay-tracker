# Mumbai Local Train Delay Tracker

Production-ready full-stack observability for Mumbai suburban rail delays across the Central, Western, and Harbour lines.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) [![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js&logoColor=white)](https://nextjs.org/) [![CI](https://github.com/lakshyakurup/mumbai-local-delay-tracker/actions/workflows/ingest-and-ci.yml/badge.svg)](https://github.com/lakshyakurup/mumbai-local-delay-tracker/actions)

## Quick deploy (production)

### 1. Backend on Render

1. Connect this repo to [Render](https://render.com).
2. Use the existing `render.yaml` Blueprint (or create a Web Service from `backend`).
3. Set environment variables:
   - `DATABASE_URL` → your Postgres connection string
   - `CORS_ORIGINS` → your Vercel domain (e.g. `https://mumbai-local.vercel.app`)
   - `SCRAPER_TOKEN` → a long random secret
4. Deploy. Note the public API URL (e.g. `https://mumbai-local-delay-tracker.onrender.com`).

### 2. Frontend on Vercel (60 seconds)

1. Go to [vercel.com/new](https://vercel.com/new) and import `lakshyakurup/mumbai-local-delay-tracker`.
2. **Root Directory** → `frontend`
3. **Environment Variable**:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: your Render API URL (no trailing slash)
4. Click **Deploy**.

That’s it. Vercel will use `frontend/vercel.json` and `next.config.mjs` automatically.

## What is included

- FastAPI v2 API with CORS, rate limiting, Prometheus metrics, health probes, typed schemas, and SQLAlchemy persistence.
- Scraper service that parses JSON feeds and announcement text, classifies severity, and records updates every 15 minutes.
- Next.js command center with live line cards, delay observations, analytics trends, station-level metrics, and responsive styling.
- Docker Compose for local development, optimized backend/frontend images, Render Blueprint deployment, and GitHub Actions automation.
- Focused pytest coverage for scraper logic and API behavior.

## API surface

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Database-backed service health |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/v2/lines/status` | Current Central, Western, and Harbour status |
| `GET` | `/api/v2/delays` | Recent delay records with line and time filters |
| `POST` | `/api/v2/delays` | Create a delay observation |
| `DELETE` | `/api/v2/delays/{record_id}` | Soft-delete an observation (requires Bearer token) |
| `GET` | `/api/v2/lines/{line}/stations` | Station reliability metrics |
| `GET` | `/api/v2/stats/summary` | Average delay and peak hour |
| `GET` | `/api/v2/stats/trends` | Daily historical delay buckets |

Interactive docs: `/docs` when the API is running.

## Local development

### Docker Compose

```bash
git clone https://github.com/lakshyakurup/mumbai-local-delay-tracker.git
cd mumbai-local-delay-tracker
cp .env.example .env
docker compose up --build
```

- Dashboard: http://localhost:3000
- API docs: http://localhost:8000/docs

### Native

```bash
# Backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
DATABASE_URL=sqlite:///./local.db SCRAPER_TOKEN=dev uvicorn backend.main:app --reload --port 8000

# Frontend (second terminal)
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

Tests:

```bash
PYTHONPATH=. pytest backend/tests -q
cd frontend && npm run build
```

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | SQLite locally or PostgreSQL in production |
| `CORS_ORIGINS` | Yes | Comma-separated frontend origins |
| `NEXT_PUBLIC_API_URL` | Frontend | Public API base URL (no trailing slash) |
| `SCRAPER_SOURCE_URL` | No | JSON or text status source |
| `SCRAPER_TOKEN` | Production | Bearer token for admin actions |
| `RATE_LIMIT` | No | Default `120/minute` |

## License

MIT — see [LICENSE](LICENSE).
