# ShareShelf
A peer-to-peer lending library for everyday tools and equipment.

## Setup
1. Create a virtual environment: `python -m venv .venv`, then activate it.
2. Install packages: `python -m pip install -r requirements.txt`
3. Create a PostgreSQL database named `shareshelf`.
4. Create a `.env` file next to `manage.py` with SECRET_KEY, DEBUG, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT.
5. Run `python manage.py migrate`, then `python manage.py createsuperuser`.
6. Start the server with `python manage.py runserver`.