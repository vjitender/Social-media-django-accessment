# Social-media-django-accessment

This README provides instructions on setting up and running a Django project with a virtual environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8
- pip (Python package manager)
- Virtualenv (for creating a virtual environment)

## Project Setup

1. Clone the project repository:
   git clone https://github.com/vjitender/Social-media-django-accessment.git
   cd Social-media-django-accessment

2. Create a virtual environment:
   python -m venv env

3. Activate the virtual environment:
   source env/bin/activate

4. Install project dependencies:
   pip install -r requirements.txt

5. Perform database migrations:
   python manage.py migrate

6. Start the development server:
   python manage.py runserver
