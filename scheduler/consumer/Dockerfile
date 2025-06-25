FROM python:3.12

WORKDIR /consumer

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["celery", "-A", "consumer", "worker", "--loglevel=info"]

