FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /busbook
ADD . .
RUN pip install -r /busbook/requirements.txt
RUN python3 manage.py makemigrations 
RUN python manage.py migrate
#RUN python manage.py runserver 0.0.0.0:8000