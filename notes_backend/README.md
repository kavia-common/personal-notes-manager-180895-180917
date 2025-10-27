# Personal Notes Backend (FastAPI)

A minimal FastAPI backend providing CRUD operations for personal notes with basic authentication scaffolding and an in-memory store.

## Quick Start

The preview management is already configured. This service exposes docs at `/docs`.

## Authentication (Scaffolding)

- Uses a placeholder dependency that reads `X-User-Id` header.
- If absent, it defaults to `anonymous`.
- TODO: Replace with real auth (JWT/session/OAuth) and enforce per-user isolation.

## Endpoints

- GET `/` — Health check.
- POST `/notes` — Create a note.
  - Body: `{ "title": "string (min 1)", "content": "string (min 1)" }`
  - Returns: `NoteOut`, 201.
- GET `/notes` — List notes for current user. Returns `NoteOut[]`.
- GET `/notes/{id}` — Get a specific note. Returns `NoteOut`, 200; 404 if not found.
- PUT `/notes/{id}` — Update a note (title/content optional). Returns `NoteOut`, 200; 400 if no fields; 404 if not found.
- DELETE `/notes/{id}` — Delete a note. Returns 204; 404 if not found.

### Schemas

- NoteCreate: `title`, `content` (both required, min length 1)
- NoteUpdate: `title?`, `content?` (at least one required)
- NoteOut: `id`, `title`, `content`, `owner_id`, `created_at`, `updated_at`

## Storage

- Thread-safe in-memory store with auto-incrementing IDs.
- Process lifetime only. TODO: Replace with a real database.

## Run Locally (if needed)

- Uvicorn is included. Example:
  ```
  uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload
  ```
- Then open `/docs`.

## Notes

- CORS is open for development; restrict in production via environment variables.
