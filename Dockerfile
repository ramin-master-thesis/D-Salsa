FROM python:3.9.1-slim-buster


WORKDIR /app
COPY . /app

RUN apt-get update \
 && apt-get install build-essential -y

RUN pip install -r requirements.txt

EXPOSE 80
ENV FLASK_APP=server

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "80"]
