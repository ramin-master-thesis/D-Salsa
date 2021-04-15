# SALSA
Small piece of code simulating the SALSA algorithm.
## Deployment
Build image from Dockerfile:
```shell
docker build -t raminqaf/salsa:1.1 .
```
## Usage
### Local
Run the command to start the server. The application needs some time to set up the indexes.
```shell
export FLASK_APP=server
flas run
```
### Docker
Run image from the root of the project:
```shell
docker run -p 5000:5001 -v $(pwd)/data:/app/data --name salsa raminqaf/salsa:1.1
```
