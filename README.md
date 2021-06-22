# SALSA

Small piece of code simulating the SALSA algorithm.

## Deployment

Build image from Dockerfile:

```shell
docker build -t raminqaf/salsa:1.3 .
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
docker run --rm -d -p <port_number>:5000 -v $(pwd)/data:/app/data raminqaf/salsa:1.3 python -m server.app --partition-method <partition_method> --partition_number <partition_number>
```

choose a free port as the `port_number`. You can choose between these partitioning methods:

| partitioning method  | number of partition   |
| -------------------- |:---------------------:|
| single_partition     | only 0                |
| murmur2              | 0 or more             |
| modulo               | 0 or more             |
| StarSpace            | 0 or more             |

**NOTE:** The `partition_number` depends on the indexed and partitioned data in the `data` folder.
