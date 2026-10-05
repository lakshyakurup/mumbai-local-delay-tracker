# Architecture & System Design — Mumbai Local Train Delay Tracker

## Overview

The production entry point is `backend.main:app`. The legacy `backend.app` package remains available for backward-compatible consumers, while all new dashboard traffic uses the versioned `/api/v2` surface.
The **Mumbai Local Train Delay Tracker** is engineered as a robust, full-stack data pipeline and real-time dashboard tracking operational delays across Mumbai's three primary suburban railway corridors: Central, Western, and Harbour lines.

## Architectural Layers

### 1. Data Ingestion & Pipeline Layer (Python)
- **Scrapers / Simulators:** Python-based asynchronous workers fetch live status feeds, platform announcements, and crowdsourced delay indicators.
- **Data Cleaner & Normalizer:** Standardizes timestamps, station codes, and line identifiers into a unified schema using Pydantic.
- `ScraperService` accepts JSON or announcement text, rejects unknown lines, classifies severity, and persists records through SQLAlchemy.
- APScheduler runs the same service every 15 minutes; GitHub Actions and Render cron can trigger the authenticated one-shot endpoint.

### 2. Backend & API Layer (FastAPI / SQLAlchemy)
- **RESTful Endpoints:** Exposes structured JSON endpoints for live delay summaries, historical trends, and line status.
- **Database ORM:** SQLAlchemy models mapping delay logs, station metrics, and incident reports to a persistent PostgreSQL/SQLite store.

### 3. Frontend Dashboard Layer (Next.js 14 / TypeScript)
- **App Router Architecture:** Server-side rendered components delivering lightning-fast initial load times.
- **Interactive Visualizations:** Tailwind CSS styling with real-time status badges, interactive route filters, and delay graphs.
- `AppProvider` owns polling state; the command center, analytics, and station detail routes consume typed API clients.

## Data Flow Diagram
[Data Source / Feeds] ---> [Python Async Pipeline] ---> [FastAPI REST Backend] ---> [PostgreSQL Store] ---> [Next.js Dashboard UI]

## Reliability boundaries

- The API health probe fails closed on database errors and exposes no credentials.
- The scheduler uses one job id and `max_instances=1` to avoid duplicate ingestion.
- SQLite is suitable for single-instance development and Render persistent disks; PostgreSQL is the production scale-out target.
- CORS origins, database URL, source URL, rate limit, and scraper token are environment-controlled.
