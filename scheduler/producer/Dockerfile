FROM python:3.12

WORKDIR /producer

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 5000

CMD ["python", "producer.py"]

