FROM python:3.9.1-alpine3.12

WORKDIR /app
COPY .. /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","app.py"]
