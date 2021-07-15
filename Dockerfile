### This is the docker file of the server, graph, and algorithem packages
### through this docker file you can create an image for starting the flask server to request recommendations

FROM python:3.8.5-slim-buster AS compile-image

RUN apt-get update \
&& apt-get install -y build-essential gcc cmake libboost-all-dev

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt -t /opt/venv

COPY ./star_space/src ./star_space/src
RUN cd ./star_space/src/python
RUN cd ./star_space/src/python && chmod +x build.sh && ./build.sh


FROM ubuntu:20.04 AS build-image

RUN apt-get update \
&& apt-get install -y python3

COPY --from=compile-image /opt/venv /app
COPY --from=compile-image /star_space/src/python/starwrap.so /app
WORKDIR /app
# Make sure we use the virtualenv:
ENV PATH="/app/bin:$PATH"
RUN ln -s /usr/bin/python3 /usr/bin/python

ADD definitions.py definitions.py
ADD ./algorithm ./algorithm
ADD ./indexer ./indexer
ADD ./partitioner ./partitioner
ADD ./server ./server
ADD ./graph ./graph

EXPOSE 5000
ENV FLASK_APP=salsa

CMD ["python", "-m", "server.app"]
