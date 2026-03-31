# 📦 Product Catalog — Django Application

A clean, fully functional Django product catalog with search, category filtering, and tag filtering built with SQLite and zero external dependencies beyond Django itself.


## Features

- Browse all products in a responsive card grid
- Full-text search across product name and description
- Filter by category (dropdown)
- Filter by one or more tags (checkboxes)
- Django admin panel with pre-configured list views, filters, and search
- One-command sample data population (21 products across 5 categories)


## Installation

### 1. Clone / enter the project directory
```bash
cd product-catalog
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py migrate
```

### 5. Populate sample data
```bash
python manage.py populate_sample_data
```

### 6. (Optional) Create a superuser for the admin panel
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.


## What Each Setup Step Does

Understanding what happens under the hood makes debugging much easier if something goes wrong.

| Step | What it does |
|------|-------------|
| `python -m venv venv` | Creates an isolated Python environment so project dependencies don't conflict with other projects on your machine |
| `pip install -r requirements.txt` | Installs Django 4.2.11 into that isolated environment |
| `python manage.py migrate` | Reads all migration files and creates the SQLite database tables (`Category`, `Tag`, `Product`, and Django's built-in auth/session tables) |
| `python manage.py populate_sample_data` | Runs a custom management command that wipes any existing catalog data and inserts 5 categories, 10 tags, and 21 products so the app is demo-ready immediately |
| `python manage.py createsuperuser` | Creates an admin account stored in the database — prompts for username, email, and password; survives server restarts |
| `python manage.py runserver` | Starts a local development server at `http://127.0.0.1:8000/` |

> **Note:** The superuser account persists in `db.sqlite3` across server restarts and reboots. The only things that would remove it are deleting `db.sqlite3` or running `python manage.py flush`.


## Usage

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Product catalog home page |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

### Searching & filtering

- **Search** — type any keyword; matches product name and description
- **Category** — pick one category from the dropdown
- **Tags** — tick one or more tag checkboxes (I am using AND logic — must have all selected tags)
- Click **Search** to apply, **Clear** to reset

### Populating data — two options

You can populate the database in either of these ways:

| Method | How | Best for |
|--------|-----|---------|
| **Management command** | `python manage.py populate_sample_data` | Getting demo data instantly; resets to clean state |
| **Admin interface** | Log in at `/admin/`, add records manually | Custom/real data; full control over each field |

> **Warning:** `populate_sample_data` deletes all existing `Category`, `Tag`, and `Product` records before re-seeding. Do not run it if you have real data you want to keep.


## Models

| Model | Key fields |
|-------|-----------|
| `Category` | `name` (unique), `description`, `created_at` |
| `Tag` | `name` (unique), `created_at` |
| `Product` | `name`, `description`, `price`, `category` (FK), `tags` (M2M), `created_at`, `updated_at` |


## Project Structure

```
.
├── .gitignore
├── requirements.txt
├── manage.py
├── README.md
├── product_catalog/          # Django project package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/                 # Products app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── commands/
│           └── populate_sample_data.py
└── templates/
    └── products/
        └── product_list.html
```

## Troubleshooting

**`ModuleNotFoundError: No module named 'django'`**
The virtual environment is not active. Django is installed inside `venv/`, not globally — Python can only find it when the environment is activated.
```bash
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

**`OperationalError: no such table`**
The database tables haven't been created yet. Migrations build the schema from the model definitions — without running them, the tables simply don't exist.
```bash
python manage.py migrate
```

**Admin panel shows no products**
The database is empty. Either run the management command to seed it, or add records manually through the admin.
```bash
python manage.py populate_sample_data
```
Then log in at `/admin/` with the superuser you created. If you haven't created one yet, run `python manage.py createsuperuser` first.

**Port already in use**
Another process (possibly a previous server instance) is already listening on port 8000. Run on a different port instead.
```bash
python manage.py runserver 8080
```

**Search returns no results after typing**
The form requires clicking **Search** to submit — there is no live/auto-filter. Make sure you clicked the green Search button after typing your query.

## 🤖 AI Disclosure

AI tools were used for assistance in two specific areas of this project:

1. **Styling and CSS** — Initial styles for the product listing template (`templates/products/product_list.html`) were generated with AI assistance, including the card grid layout, sidebar filter panel, colour scheme, and responsive breakpoints.

2. **Sample mock data** — Product names, descriptions, and prices in the `populate_sample_data` management command were generated with AI assistance to provide a realistic and varied demo dataset across the five categories.

All AI-generated code was reviewed, understood, tested, and modified to meet the project requirements. The core application logic including models, views, URL routing, query optimisation, and admin configuration was written and reasoned through independently.

This disclosure is made in accordance with the AI usage policy. AI was used as a productivity tool, not as a replacement for understanding the code.
