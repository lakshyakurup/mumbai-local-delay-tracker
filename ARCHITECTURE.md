# Architecture & System Design — Mumbai Local Train Delay Tracker

## Overview
The **Mumbai Local Train Delay Tracker** is engineered as a robust, full-stack data pipeline and real-time dashboard tracking operational delays across Mumbai's three primary suburban railway corridors: Central, Western, and Harbour lines.

## Architectural Layers

### 1. Data Ingestion & Pipeline Layer (Python)
- **Scrapers / Simulators:** Python-based asynchronous workers fetch live status feeds, platform announcements, and crowdsourced delay indicators.
- **Data Cleaner & Normalizer:** Standardizes timestamps, station codes, and line identifiers into a unified schema using Pydantic.

### 2. Backend & API Layer (FastAPI / SQLAlchemy)
- **RESTful Endpoints:** Exposes structured JSON endpoints for live delay summaries, historical trends, and line status.
- **Database ORM:** SQLAlchemy models mapping delay logs, station metrics, and incident reports to a persistent PostgreSQL/SQLite store.

### 3. Frontend Dashboard Layer (Next.js 14 / TypeScript)
- **App Router Architecture:** Server-side rendered components delivering lightning-fast initial load times.
- **Interactive Visualizations:** Tailwind CSS styling with real-time status badges, interactive route filters, and delay graphs.

## Data Flow Diagram
[Data Source / Feeds] ---> [Python Async Pipeline] ---> [FastAPI REST Backend] ---> [PostgreSQL Store] ---> [Next.js Dashboard UI]
