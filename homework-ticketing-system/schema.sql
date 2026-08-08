-- Schema + sample data for the Lakebase-powered support ticketing app.
-- Run this once in your Lakebase Postgres database (SQL editor or psql)
-- before starting the app.

CREATE TABLE IF NOT EXISTS tickets (
    ticket_id   SERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'open'
                CHECK (status IN ('open', 'in_progress', 'resolved')),
    priority    TEXT NOT NULL DEFAULT 'normal'
                CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    category    TEXT,
    created_by  TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS ticket_messages (
    message_id    SERIAL PRIMARY KEY,
    ticket_id     INTEGER NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    message_text  TEXT NOT NULL,
    author        TEXT NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_ticket_messages_ticket_id ON ticket_messages (ticket_id);

-- Sample data: 4 tickets across 3 statuses, 2+ messages each.

INSERT INTO tickets (title, status, priority, category, created_by) VALUES
    ('Login page returns 500 error', 'open', 'high', 'bug', 'alice'),
    ('Add dark mode toggle', 'in_progress', 'low', 'feature-request', 'bob'),
    ('Password reset email not sending', 'resolved', 'urgent', 'bug', 'carol'),
    ('Slow dashboard load times', 'open', 'normal', 'performance', 'dave');

INSERT INTO ticket_messages (ticket_id, message_text, author) VALUES
    (1, 'Getting a 500 error every time I try to log in since this morning.', 'alice'),
    (1, 'Can confirm - same error on staging. Looking into the logs now.', 'support-eng'),
    (2, 'Would love a dark mode option, the white background is rough at night.', 'bob'),
    (2, 'Started work on this, targeting next release.', 'support-eng'),
    (3, 'Requested a password reset an hour ago, no email has arrived.', 'carol'),
    (3, 'Found it - our email provider had a delivery delay. Should be resolved now, please confirm.', 'support-eng'),
    (3, 'Got it, thanks! Working now.', 'carol'),
    (4, 'Dashboard takes 10+ seconds to load with a large watchlist.', 'dave'),
    (4, 'Reproduced locally, looking at the query plan.', 'support-eng');

-- Verify:
-- SELECT * FROM tickets ORDER BY ticket_id;
-- SELECT * FROM ticket_messages ORDER BY ticket_id, created_at;
