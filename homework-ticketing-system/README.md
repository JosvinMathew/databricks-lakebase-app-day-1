# Day 1 Homework: Lakebase-Powered AI Support App

A Flask + Lakebase support ticketing app — same connection pattern as the Day 1-3 apps (single `LAKEBASE_URL` secret, resolved via the Databricks SDK at runtime, never in a file).

## What's here

- `schema.sql` — `tickets` + `ticket_messages` tables (with `ticket_messages.ticket_id` referencing `tickets`, `ON DELETE CASCADE`), plus sample data: 4 tickets across 3 statuses, 2-3 messages each
- `lakebase.py` — connection helper (same pattern as Day 1-3)
- `app.py` — Flask app: list/filter tickets, view a ticket + its messages, create a ticket, add a message, update status, delete a ticket
- `templates/index.html`, `templates/ticket.html` — the UI
- `setup_secrets.py` — stores the Lakebase URL secret (skip if reusing Day 1-3's `database/lakebase-url` secret in the same workspace)
- `app.yaml` / `requirements.txt` / `.env.example` — Databricks App config + local dev

## Requirements checklist

- [x] `tickets` table: `ticket_id`, `title`, `status`, `created_by`, `created_at` (+ `priority`, `category`)
- [x] `ticket_messages` table: `message_id`, `ticket_id` (FK), `message_text`, `author`, `created_at`
- [x] Sample data: 4 tickets, 2-3 statuses represented, 2+ messages per ticket
- [x] View all tickets
- [x] Select a ticket and view its messages
- [x] Create a new ticket
- [x] Add a message to an existing ticket
- [x] Update a ticket's status
- [x] Reads and writes go through Lakebase, no hard-coded app data
- [ ] Deployed to Databricks Apps and verified (do this in your workspace — see below)

## Bonus challenges implemented

- [x] Ticket priority (`low`/`normal`/`high`/`urgent`) and category
- [x] Filtering by status
- [x] Input validation with flashed error messages (missing title/name/message, invalid status/priority)
- [x] Ticket statistics (total + per-status counts on the ticket list)
- [x] Delete with a confirmation step (`confirm()` before the delete form submits)
- [x] Styled UI (status/priority badges, stat cards, filter pills)

## Setup

### 1. Run the schema

In a Databricks SQL editor connected to your Lakebase instance (or `psql` with your `LAKEBASE_URL`), run `schema.sql`. Reuse the same Lakebase instance from Day 1-3 if you have one — this just adds two new tables to it.

### 2. Store the secret (skip if reusing Day 1-3's)

```
%sh python setup_secrets.py
```
from a Databricks notebook, same as the earlier days.

### 3. Local dev

```bash
cp .env.example .env   # paste your Lakebase URL
pip install -r requirements.txt
python app.py           # serves on :8000
```

### 4. Deploy to Databricks Apps

Same flow as [Day 1's step 7](../../day-1-lakebase-simple-application/app/README.md#7-create-a-git-folder-in-databricks-and-deploy-the-app-no-cli-required): create/reuse a Git folder for this repo, create a Databricks App pointed at this folder (so it picks up `app.yaml`), deploy, then confirm:
- Existing tickets load from Lakebase
- A new ticket can be created
- A message can be added
- A ticket's status can be updated
- Changes remain after refreshing

## Submission checklist

- [ ] Databricks App URL
- [ ] Source code, zipped
- [ ] Screenshot of the deployed app
- [ ] Screenshot of the Lakebase tables + sample records
- [ ] 3-5 sentence reflection: hardest part, how Lakebase differs from a traditional analytics table, what feature you'd add next

Don't include real credentials/API keys/passwords in the zip or screenshots.

**From the instructor directly (not in the original assignment text):** *"Instructors don't need access to the app. Just upload good screenshots and that's good enough!"* — so a live, currently-reachable App URL isn't actually required for grading, just good screenshots + the zipped code. Submit through the assignment platform (zip upload, not a GitHub link) — resubmitting is unlimited, only your last submission before the deadline counts.
