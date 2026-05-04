# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Manoli Bakes** is a Django 5 application for managing bakery orders. Customers place orders for specific bread types on given dates. The app tracks recurring defaults and per-day overrides.

## Architecture

### Django Apps

- **`core/`** — Main bakery logic: models, views, forms, services, DTOs, utils.
- **`members/`** — Authentication only (login/logout). No custom models.

### Request Flow

```
URL (urls.py) → View (views.py) → Service (services/) → Model or raw SQL → Template
```

Views are all function-based and protected with `@login_required`.

### Service Layer

Business logic lives in `core/services/`:

- **`orders.py`** — Aggregated daily totals across all customers (`get_orders`).
- **`customer.py`** — Per-customer order resolution (`get_customer_final_orders`, `save_customer_data`, daily defaults).

Services use raw SQL via `django.db.connection` for complex aggregations. Do not replace these with ORM queries without verifying equivalent behavior.

### Order Resolution Logic

Orders for a customer+bread+date are resolved with this priority:
1. If an `Order` row exists for that date → use its `number`.
2. Else if a `DailyDefaults` row exists → use its `number`.
3. Else → 0.

`save_customer_data` in `customer.py` implements the inverse: it only writes an `Order` row when the submitted value differs from the daily default, and deletes existing `Order` rows when the value matches the default.

### DTOs

`core/dto.py` defines Pydantic models used as the return type of service functions. The only DTO currently is `OrderDTO(id, name, number)`.

### Data Models (`core/models.py`)

- **`Customer`** — `name`, `lastname` (unique together).
- **`Bread`** — `name`.
- **`Order`** — `customer`, `bread`, `date`, `number` (unique on customer+bread+date).
- **`DailyDefaults`** — `customer`, `bread`, `number` (unique on customer+bread). Acts as a standing order.

### Database

- **Development:** SQLite at `../data/db.sqlite3` (relative to `manolibakes/`).
- **Production:** PostgreSQL 14 via Docker Compose, configured through `debug.env`.

### Authentication

Session-based auth using Django's built-in system. Cookie timeout: 1 hour (`SESSION_COOKIE_AGE = 3600`). All core views require login.

## UI

Always use DESIGN.md for UI work.
