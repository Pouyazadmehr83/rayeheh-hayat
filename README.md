# Rayeheh-Hayat — Perfume & Fragrance Showcase (Flask)

Rayeheh-Hayat is a Flask-based web application for discovering, reviewing, and showcasing perfumes and colognes. The project emphasizes the Flask technology stack and provides features typical of a perfume-introduction/review site.

Repository: https://github.com/Pouyazadmehr83/rayeheh-hayat

## Project summary

Rayeheh-Hayat is designed to be a modern, responsive website where users can:

- Browse curated perfume profiles (brand, notes, launch year, longevity, sillage)
- Read and write reviews and ratings for perfumes
- Search and filter perfumes by brand, notes, or rating
- View suggested/related perfumes and match recommendations
- Manage user profiles and favorites (optional)
- Admin management of entries and reviews

The project also may include C/C++ or Cython components to accelerate specific tasks (e.g., similarity computations or text processing), but the core web app is built with Flask.

## Technologies

- Python 3.8+
- Flask (Blueprints, Flask-Login, Flask-Migrate recommended)
- SQLAlchemy (ORM)
- Flask-Migrate (Alembic) for database migrations
- Jinja2 templates, Bootstrap or custom SCSS for UI
- Optional native extensions: C/C++/Cython for performance-sensitive functions
- Optional PostgreSQL for production

## Requirements

- Git
- Python 3.8+
- pip
- virtualenv (recommended)
- C/C++ toolchain if native extensions must be built

## Installation — exact steps (local development)

1. Clone the repository
   git clone https://github.com/Pouyazadmehr83/rayeheh-hayat.git
   cd rayeheh-hayat

2. Create and activate a virtual environment
   # macOS / Linux
   python -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Install dependencies
   pip install -r requirements.txt

4. (If native extensions exist) Ensure compiler toolchain is installed
   - Ubuntu: sudo apt-get install build-essential python3-dev
   - macOS: xcode-select --install
   - Windows: Install Visual Studio Build Tools

   Then build extensions (if applicable):
   python setup.py build_ext --inplace
   or
   pip install -e .

5. Configure environment variables
   Create a `.env` file or export variables:
   FLASK_APP=run.py          # or the app entrypoint
   FLASK_ENV=development
   SECRET_KEY=replace_with_secure_key
   DATABASE_URL=sqlite:///dev.db   # or your PostgreSQL URL

6. Initialize and migrate the database (Flask-Migrate)
   flask db init           # only if migrations directory is not present
   flask db migrate -m "Initial migration"
   flask db upgrade

7. Create an admin user (if helper command exists) or create via shell

8. Run the development server
   flask run --host=0.0.0.0 --port=5000
   Open http://localhost:5000

## Running with Gunicorn (production example)

1. Set FLASK_ENV=production and set proper SECRET_KEY.
2. Run Gunicorn:
   gunicorn "run:create_app()" --bind 0.0.0.0:8000 --workers 3
   Replace `run:create_app()` with the actual application factory if present.

Use Nginx to serve static files and reverse-proxy to Gunicorn.

## Suggested features for a perfume site

- Rich perfume pages with pyramid of notes, user ratings, and reviews
- Search by top notes, heart notes, base notes, brand, and year
- Similarity-based recommendations (can be accelerated with native modules)
- Admin UI to curate highlights and featured perfumes

## Testing & QA

- Run tests:
  pytest -q

## License & Contact

- Add a LICENSE file (e.g., MIT) to clarify terms.
- Author: Pouyazadmehr83
