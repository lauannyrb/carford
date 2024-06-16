FROM python:3.12

WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY .env .env

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${API_PORT}

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "${API_PORT}"]
