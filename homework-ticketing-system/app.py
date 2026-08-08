import os
import secrets

from flask import Flask, flash, redirect, render_template, request, url_for

from lakebase import run_query, run_write

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))

STATUSES = ["open", "in_progress", "resolved"]
PRIORITIES = ["low", "normal", "high", "urgent"]


@app.route("/healthz")
def healthz():
    return {"status": "ok"}


@app.route("/")
def index():
    status_filter = request.args.get("status", "")
    if status_filter not in STATUSES:
        status_filter = ""

    if status_filter:
        tickets = run_query(
            """
            SELECT ticket_id, title, status, priority, category, created_by, created_at
            FROM tickets
            WHERE status = %(status)s
            ORDER BY created_at DESC
            """,
            {"status": status_filter},
        )
    else:
        tickets = run_query(
            """
            SELECT ticket_id, title, status, priority, category, created_by, created_at
            FROM tickets
            ORDER BY created_at DESC
            """
        )

    stats_rows = run_query("SELECT status, COUNT(*) AS count FROM tickets GROUP BY status")
    stats = {row["status"]: row["count"] for row in stats_rows}
    total = sum(stats.values())

    return render_template(
        "index.html",
        tickets=tickets,
        statuses=STATUSES,
        priorities=PRIORITIES,
        status_filter=status_filter,
        stats=stats,
        total=total,
    )


@app.route("/tickets", methods=["POST"])
def create_ticket():
    title = request.form.get("title", "").strip()
    created_by = request.form.get("created_by", "").strip()
    priority = request.form.get("priority", "normal")
    category = request.form.get("category", "").strip() or None

    errors = []
    if not title:
        errors.append("Title is required.")
    if not created_by:
        errors.append("Your name is required.")
    if priority not in PRIORITIES:
        errors.append("Invalid priority.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("index"))

    run_write(
        """
        INSERT INTO tickets (title, status, priority, category, created_by)
        VALUES (%(title)s, 'open', %(priority)s, %(category)s, %(created_by)s)
        """,
        {"title": title, "priority": priority, "category": category, "created_by": created_by},
    )
    flash(f'Ticket "{title}" created.', "success")
    return redirect(url_for("index"))


@app.route("/ticket/<int:ticket_id>")
def ticket_detail(ticket_id):
    rows = run_query("SELECT * FROM tickets WHERE ticket_id = %(id)s", {"id": ticket_id})
    if not rows:
        flash("Ticket not found.", "error")
        return redirect(url_for("index"))

    messages = run_query(
        "SELECT * FROM ticket_messages WHERE ticket_id = %(id)s ORDER BY created_at ASC",
        {"id": ticket_id},
    )
    return render_template("ticket.html", ticket=rows[0], messages=messages, statuses=STATUSES)


@app.route("/ticket/<int:ticket_id>/messages", methods=["POST"])
def add_message(ticket_id):
    message_text = request.form.get("message_text", "").strip()
    author = request.form.get("author", "").strip()

    errors = []
    if not message_text:
        errors.append("Message text is required.")
    if not author:
        errors.append("Author name is required.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("ticket_detail", ticket_id=ticket_id))

    run_write(
        """
        INSERT INTO ticket_messages (ticket_id, message_text, author)
        VALUES (%(ticket_id)s, %(message_text)s, %(author)s)
        """,
        {"ticket_id": ticket_id, "message_text": message_text, "author": author},
    )
    flash("Message added.", "success")
    return redirect(url_for("ticket_detail", ticket_id=ticket_id))


@app.route("/ticket/<int:ticket_id>/status", methods=["POST"])
def update_status(ticket_id):
    status = request.form.get("status", "")
    if status not in STATUSES:
        flash("Invalid status.", "error")
        return redirect(url_for("ticket_detail", ticket_id=ticket_id))

    run_write(
        "UPDATE tickets SET status = %(status)s WHERE ticket_id = %(id)s",
        {"status": status, "id": ticket_id},
    )
    flash(f"Status updated to {status}.", "success")
    return redirect(url_for("ticket_detail", ticket_id=ticket_id))


@app.route("/ticket/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket(ticket_id):
    run_write("DELETE FROM tickets WHERE ticket_id = %(id)s", {"id": ticket_id})
    flash("Ticket deleted.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)
