# D-SALSA

Piece of code simulating the D(istributed)-SALSA algorithm and a simple indexing system for traversing the bipartite graph.

## Prerequisites

* Clone the repository on your computer.
* Create a python virtual environment and run `pip install -r requirements.txt`. This will install all the necessary
  dependencies.
* The crawled datasets (train and test) plus the generated train dataset can be
  found [here](https://mega.nz/folder/BQhzVQBD#_7EQ9ujrU2irq-BRfNOUdw). Place the test dataset in the `data` folder.
* Create a `StarSpace_data` folder inside the `data` folder and move the train dataset there.
* Inside the `StarSpace_data` folder create a `models` directory. You need to place your trained model folder(s) here.
* The dataset(s) should be in a TSV or CSV format.
* Here is an example how the dataset should look like:

```tsv
34743251   1336849897987796992    0  1607564827000  Starship landing flip maneuver https://t.co/QuD9HwZ9CX
44196397   1336810077555019779    0  1607555333000  Mars, here we come!!
44196397   1336808486022258688    0  1607554954000  Successful ascent, switchover to header tanks & precise flap control to landing point! https://t.co/IIraiESg5M
34743251   1336777137391456256    0  1607547480000  Watch Starship high-altitude test live → https://t.co/Hs5C53qBxb https://t.co/sEMe4firi6
34743251   1336441306944454656    0  1607467412000  Raptor auto-abort at T-1 second
...
```

## Usage Partitioner

The partitioner shards the data based on the strategy it was initialized. Furthermore, it creates the indexes for each
partition and saves the results in the `data` folder.

### Local

The following command will run the partitioner and afterward the indexer:

```shell
python3 -m partitioner.main [OPTIONS] COMMAND [ARGS]...

Options:
  -f, --path-to-file TEXT         path to the tsv data file (default is
                                  /data/tweets-dump.tsv)

  --content-index / --no-content-index
                                  A flag dedicating if the content index
                                  should be generated or not (default is
                                  false)

  --help                          Show this message and exit.

Commands:
  modulo
  murmur2
  single
  star-space
```

Choosing the `murmur2` segmentation method:

```shell
python3 -m partitioner.main murmur2 [OPTIONS]

Options:
  -n, --partition-number INTEGER  total number of partitions (default 2)
  --help                          Show this message and exit.

```

Choosing the `star-space` partitioning method:

```shell
python3 -m partitioner.main star-space [OPTIONS]

Options:
  -n, --partition-number INTEGER  total number of partitions (default 2)
  -m, --model-folder TEXT         folder name of the model parameter
                                  [required]

  --help                          Show this message and exit.

```

The `--model-folder` option is required for partitioning with StarSpace. This option determines the model that needs to
be loaded in memory. The folder should be inside the following path: `data > StarSpace_data > models`.
<br/> After the partitioning and indexing finishes, you can find it in the `data` folder. Depending on the partitioning
method and total count of partitions chosen, the number of folders varies.

## Usage SALSA Webserver

The webserver loads the partitioned and index data in memory and provides API endpoints to generate recommendations with
the SALSA algorithm. Moreover, it offers access to the indexer for gathering meta information like the total number of
edges, nodes, and other information like the degree of the user.

### Local

Run the command to start the server. The application needs some time to set up the indexes.

```shell
python3 -m server.app [OPTIONS]

Options:
  --partition-method [single|modulo|murmur2|star-space]
                                  hash function used for partitioning
                                  (defaults single).

  --partition-id INTEGER      id of partition
  --port INTEGER              port number of server
  --content-index / --no-content-index
                                  Flag whether to load content index or not
  --help                          Show this message and exit.

```

### Docker

Run image from the root of the project:

```shell
docker run --rm -d -p <port_number>:5000 -v $(pwd)/data:/app/data raminqaf/salsa:1.4 python -m server.app [OPTIONS]
```

Choose a free port for the `port_number`. The volume needs to contain the indexed data. You can choose between these
partitioning methods:

| partitioning method  | ID of partition   |
| -------------------- |:---------------------:|
| single_partition     | only 0                |
| murmur2              | 0 or greater          |
| modulo               | 0 or greater          |
| StarSpace            | 0 or greater          |

Based on the partitioning method chosen, the webserver looks in the `data` folder and then searches for the desired
partition. The partition folder is chosen depending on the `partition_id` passed. The webserver then loads the left,
right, (if selected) context index in memory.

### Deployment

Build an image from Dockerfile:

```shell
docker build -t salsa:1.4 .
```

**TIP:** If you already have the partitions ready and want to run multiple servers simultaneously, execute the `run.sh`
file. You can do this like this:

```shell
bash run.sh <PARTITION_COUNT> <START_PORT> <PARTITION_METHOD>
```
