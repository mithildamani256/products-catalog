# 📦 Product Catalog — Django Application

A clean, fully functional Django product catalog with search, category filtering, and tag filtering built with SQLite and zero external dependencies beyond Django itself.

---

## Features

- Browse all products in a responsive card grid
- Full-text search across product name and description
- Filter by category (dropdown)
- Filter by one or more tags (checkboxes)
- Django admin panel with pre-configured list views, filters, and search
- One-command sample data population (21 products across 5 categories)

---

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

---

## Usage

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Product catalog home page |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

### Searching & filtering

- **Search** — type any keyword; matches product name and description
- **Category** — pick one category from the dropdown
- **Tags** — tick one or more tag checkboxes (AND logic — must have all selected tags)
- Click **Search** to apply, **Clear Filters** to reset

---

## Models

| Model | Key fields |
|-------|-----------|
| `Category` | `name` (unique), `description`, `created_at` |
| `Tag` | `name` (unique), `created_at` |
| `Product` | `name`, `description`, `price`, `category` (FK), `tags` (M2M), `created_at`, `updated_at` |

---

## Project structure

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

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'django'`**
Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

**`OperationalError: no such table`**
Run `python manage.py migrate` before starting the server.

**Admin panel shows no products**
Run `python manage.py populate_sample_data` to seed the database, then log in at `/admin/` with the superuser you created.

**Port already in use**
Run the server on a different port: `python manage.py runserver 8080`
