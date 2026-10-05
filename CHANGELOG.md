## [2.0.0] - 2026-10-05

### Added

- Versioned FastAPI `/api/v2` routes for line status, delay CRUD, station metrics, health, trends, and commuter analytics.
- SQLAlchemy models for delay records, line status, and station reliability metrics.
- JSON/text scraper parser with severity classification and 15-minute scheduler.
- Next.js command center, analytics, and station corridor views with typed polling state and Recharts trends.
- Docker, Render, GitHub Actions CI, scheduled scraper heartbeat, SQL schema, and focused backend/frontend tests.

# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-08-30
### Added
- Initial release of Mumbai Local Train Delay Tracker.
- Python data pipeline for Central, Western, and Harbour lines.
- FastAPI backend with SQLAlchemy data models.
- Next.js 14 App Router dashboard with live status badges.
- Vercel and Render deployment configuration.
