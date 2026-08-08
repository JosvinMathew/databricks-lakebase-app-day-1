# Support Ticketing System

A small support ticketing app: view tickets, open one to see its message thread, add new messages, and update status — backed by a real Postgres database.

## Features

- Ticket list with status/priority badges, live counts, and status filtering
- Create a new ticket (title, priority, category)
- Ticket detail view with full message thread
- Add a message to a ticket
- Update a ticket's status (`open` → `in_progress` → `resolved`)
- Delete a ticket (with confirmation)

## Stack

- Python / Flask, server-rendered with Jinja templates
- PostgreSQL (via `psycopg2`)
- Database credentials resolved at runtime, never stored in code or committed files

## Structure

```
app.py               Flask routes
lakebase.py           Database connection helper
schema.sql            Table definitions + sample data
templates/            UI (index + ticket detail)
```

## Running locally

```bash
pip install -r requirements.txt
cp .env.example .env      # fill in your database connection string
python app.py              # serves on :8000
```

## Setup

1. Run `schema.sql` against your Postgres database once, to create the tables and load sample data.
2. Set your database connection string (see `.env.example`).
3. Install dependencies and run (`pip install -r requirements.txt && python app.py`).
