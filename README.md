# 💪 GymBro 

A gym workout tracker built with Django.

## Features
- Track exercises by muscle group and difficulty
- Create and manage workout plans
- Log training sessions and personal records
- User registration and authentication (members cannot be managed by anyone other than admin)
- Search and filtering across all models

## Setup

1. Clone the repository
2. Create virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Run migrations:
   python manage.py migrate
5. Load sample data:
   python manage.py loaddata tracker/fixtures/initial_data.json
6. Create superuser:
   python manage.py createsuperuser
7. Run server:
   python manage.py runserver

## Tech Stack
- Python 3.13
- Django 6.x
- Bootstrap 5
- SQLite