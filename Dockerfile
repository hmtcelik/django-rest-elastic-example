FROM python:3.11-slim-buster

# this is required for Python to not write pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# just copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# then copy the rest of the files
COPY . /app/

CMD python3 manage.py collectstatic --noinput && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
