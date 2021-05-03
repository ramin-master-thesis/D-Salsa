### This is the docker file of the server, graph, and algorithem packages
### through this docker file you can create an image for starting the flask server to request recommendations

FROM python:3.8.5-slim-buster AS compile-image

RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.8.5-slim-buster AS build-image
COPY --from=compile-image /opt/venv /app
WORKDIR /app
# Make sure we use the virtualenv:
ENV PATH="/app/bin:$PATH"
COPY ./algorithm ./algorithm
COPY ./server ./server
COPY ./graph ./graph

EXPOSE 5000
ENV FLASK_APP=salsa

CMD ["python", "-m", "server.app"]
