# Django Capstone Project

## Run with venv
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Run with Docker
docker build -t capstone-app .
docker run -p 8000:8000 capstone-app
