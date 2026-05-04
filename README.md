# Manoli Bakes

A small Django 5 web app for managing daily bread orders at a bakery. Customers have standing orders (daily defaults) that get automatically applied each day, and the baker can override quantities for any specific date when things change.

## How it works

Each customer regularly orders certain quantities of bread. Instead of entering everything from scratch every day, you set up a **daily default** per customer and bread type. On any given day the baker opens the app, sees all orders pre-filled from those defaults, and adjusts only what's different that day. The app saves only the overrides — if a value matches the default it doesn't write anything, keeping the database clean.

## Apps

**`core/`** — The heart of the application. Handles all bakery logic: viewing and editing daily orders, aggregating totals across all customers, and managing the default standing orders. All views are login-protected.

**`members/`** — Handles authentication only (login and logout). No custom models, just Django's built-in auth wired up to templates.

## Entities

**Customer** — A bakery customer identified by first and last name (unique together).

**Bread** — A bread type (baguette, sourdough, etc.).

**Order** — A specific quantity of a bread type for a customer on a particular date. Only created when the quantity differs from the daily default for that day.

**DailyDefaults** — The standing daily order for a customer + bread combination. This is what gets pre-filled every morning. One row per customer/bread pair.

## Order resolution

When the baker loads orders for a given date, each customer+bread combination resolves like this:

1. If there's an `Order` row for that specific date → use it.
2. Else if there's a `DailyDefaults` row → use that.
3. Else → 0.

## Setup

Make sure you have [uv](https://docs.astral.sh/uv/) installed, then from the repo root:

```bash
uv sync
```

For development, the app uses SQLite out of the box — no extra setup needed. Just run the migrations and start the server:

```bash
cd manolibakes
uv run python manage.py migrate
uv run python manage.py runserver
```

Then open http://127.0.0.1:8000 and log in with a Django superuser account. You can create one with:

```bash
uv run python manage.py createsuperuser
```

## Commands

All commands run from the `manolibakes/` directory:

```bash
# Start development server
uv run python manage.py runserver

# Apply pending migrations
uv run python manage.py migrate

# Create new migrations after model changes
uv run python manage.py makemigrations

# Run the full test suite
uv run python manage.py test

# Run tests for a specific app
uv run python manage.py test core.tests

## Database

Development uses SQLite at `data/db.sqlite3`. Configure the database and other settings via environment variables.
