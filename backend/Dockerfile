FROM python:3.9

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:80"]