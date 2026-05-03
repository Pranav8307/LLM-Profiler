# LLM Profiler

A full-stack tool to benchmark and monitor LLM API calls. Send prompts, track latency, token usage, and cost per request, with Redis caching and a live analytics dashboard.

Built with FastAPI + PostgreSQL + Redis on the backend, and React + Tailwind + Recharts on the frontend.

---

## Features

- **Prompt → Response pipeline** — send prompts via the UI, get responses from Groq (Llama 3.1)
- **Per-request metrics** — latency (ms), token count, estimated cost per call
- **Redis caching** — cache hits skip the LLM call entirely; cost savings tracked
- **Analytics dashboard** — total requests, avg latency, total tokens, cache hit rate, cost saved
- **Call history** — paginated log of all requests with per-row metrics
- **LLM profiles** — named configurations (provider + model + params) for A/B comparisons
- **Rate limiting** — per-user request throttling
- **Dockerized** — Postgres + Redis + FastAPI all wired via docker-compose

---

## Architecture

```
React (Vite + Tailwind)
        │
        │ HTTP (axios)
        ▼
FastAPI  /api/v1
    ├── /generate      ← prompt in, response + metrics out
    ├── /logs          ← call log CRUD + per-profile stats
    ├── /profiles      ← LLM config profiles
    ├── /analytics     ← aggregated stats
    ├── /history       ← recent request history
    └── /health        ← liveness check

FastAPI → PostgreSQL  (SQLAlchemy + Alembic)
        → Redis       (response caching, rate limiting)
        → Groq API    (LLM inference)
```

---

## Quick start

### Prerequisites

- Docker + Docker Compose
- Node.js 18+ (for frontend)
- A [Groq API key](https://console.groq.com) (free)

### 1. Clone

```bash
git clone https://github.com/yourusername/LLM-Profiler.git
cd LLM-Profiler
```

### 2. Configure the backend

```bash
cd backend
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql://profiler_user:profiler_pass@localhost:5432/llm_profiler
REDIS_URL=redis://localhost:6379/0
GROQ_API_KEY=your_groq_key_here
SECRET_KEY=any_random_string_here
APP_ENV=development
DEBUG=true
```

### 3. Start backend services

```bash
# From backend/
docker-compose up -d
```

This starts Postgres, Redis, and the FastAPI server. API available at `http://localhost:8000`.

Run migrations (first time only):

```bash
docker exec llm_profiler_api alembic upgrade head
```

Swagger docs: `http://localhost:8000/docs`

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## Project structure

```
LLM-Profiler/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Route handlers
│   │   ├── core/               # Config, logging, exceptions
│   │   ├── db/                 # SQLAlchemy session, base, init
│   │   ├── models/             # ORM models (Profile, LLMCallLog, RequestLog)
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic (LLM, cache, analytics, rate limit)
│   │   └── main.py             # App factory
│   ├── migrations/             # Alembic migrations
│   ├── tests/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    ├── src/
    │   ├── components/         # PromptBox, MetricsCards, HistoryTable, Charts, AnalyticsPanel
    │   ├── App.jsx
    │   └── api.js              # Axios wrappers
    ├── package.json
    └── vite.config.js
```

---

## API reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/generate` | Send a prompt, get response + metrics |
| `GET` | `/api/v1/analytics` | Aggregated stats (latency, cost, cache rate) |
| `GET` | `/api/v1/history` | Recent request history |
| `GET` | `/api/v1/logs` | All call logs, filterable by profile/status |
| `GET` | `/api/v1/logs/stats/{profile_id}` | Per-profile aggregate stats |
| `POST` | `/api/v1/profiles` | Create an LLM profile |
| `GET` | `/api/v1/profiles` | List profiles |
| `PATCH` | `/api/v1/profiles/{id}` | Update a profile |
| `DELETE` | `/api/v1/profiles/{id}` | Delete a profile |
| `GET` | `/api/v1/health` | Health check |

Full interactive docs at `/docs` (when `DEBUG=true`).

---

## Running tests

```bash
cd backend
pytest tests/
```

---

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| Database | PostgreSQL 16 |
| Cache / Rate limiting | Redis 7 |
| LLM | Groq (Llama 3.1 8B / 70B) |
| Frontend | React 19, Vite, Tailwind CSS v4, Recharts |
| Infra | Docker, Docker Compose |
