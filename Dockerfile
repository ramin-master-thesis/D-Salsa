FROM python:3.8.5-slim-buster

WORKDIR /app
COPY . /app

RUN apt-get update \
 && apt-get install build-essential -y

RUN pip install -r requirements.txt

EXPOSE 5000
ENV FLASK_APP=salsa

CMD ["python", "-m", "server.app"]
