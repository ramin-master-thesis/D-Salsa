#!/bin/bash

trap _ctrl_c INT

_ctrl_c() {
  echo "** graceful shutdown"
  curl http://localhost:5001/shutdown
  curl http://localhost:5003/shutdown
  curl http://localhost:5002/shutdown
  curl http://localhost:5005/shutdown
  curl http://localhost:5004/shutdown
  printf "\n"
}

deploy_container() {
  PORT=$1
  PARTITION_METHOD=$2
  PARTITION_NUMBER=$3
  docker run --rm -d -p "$PORT":5000 -v $(pwd)/data:/app/data raminqaf/salsa:1.1 python -m server.app --partition-method "$PARTITION_METHOD" --partition-number "$PARTITION_NUMBER"
}

check_health() {
  PORT=$1
  printf 'start container... Doing health check... \n'
  until $(curl --output /dev/null --silent --head --fail http://0.0.0.0:"$PORT"/healthy); do
    printf '.'
    sleep 5
  done
}

stop_container() {
  PORT=$1
  curl http://localhost:$PORT/shutdown
}

if [ -z "$1" ]
  then
    echo "No arguments supplied. Please pass the number of partitions 2, 4, 8,..."
    exit 1
fi
NUMBER_OF_PARTITION=$1
CURRENT_DIRECTORY=$(pwd)

#### single_partition

PARTITION_METHOD="single"

### Partition and Index Data
#python3 -m partitioner.main "$PARTITION_METHOD"

#deploy_container "5001" "single_partition" "0"
#check_health "5001"

### murmur2

PARTITION_METHOD="murmur2"

### Partition and Index Data
python3 -m partitioner.main "$PARTITION_METHOD" -n "$NUMBER_OF_PARTITION"

### murmur2 Server
START_PORT=5002
END_PORT=0
for ((i=0;i<NUMBER_OF_PARTITION;++i)); do
  PORT=$(( $START_PORT + $i))
  deploy_container $PORT $PARTITION_METHOD $i
  END_PORT=$(( $PORT + 1))
done

for ((i=0;i<NUMBER_OF_PARTITION;++i)); do
  PORT=$(( $START_PORT + $i))
  check_health $PORT
done


### Evaluate murmur2
printf "waiting for servers to start"
cd ../evaluation/
python3 -m main
cd output

if [ ! -d murmur2 ]; then
  mkdir murmur2
fi
ls -p | grep -v / | xargs mv -t murmur2
cd $CURRENT_DIRECTORY


## Kill Container
for ((i=0;i<NUMBER_OF_PARTITION;++i)); do
  PORT=$(( $START_PORT + $i))
  stop_container $PORT
done

for f in ./data/StarSpace_data/models/*; do
  if [ -d "$f" ]; then
    # Will not run if no directories are available
    PARTITION_METHOD="star-space"
    MODEL_FOLDER=$(basename "$f")
    echo "$MODEL_FOLDER"

    ### Partition and Index Data
    python3 -m partitioner.main "$PARTITION_METHOD" -m "$MODEL_FOLDER" -n "$NUMBER_OF_PARTITION"

    ### star-space Server
    START_PORT=5002
    for ((i=0;i<NUMBER_OF_PARTITION;++i)); do
      PORT=$(( $START_PORT + $i))
      deploy_container $PORT $PARTITION_METHOD $i
    done

    for ((i=0;i<NUMBER_OF_PARTITION;++i)); do
      PORT=$(( $START_PORT + $i))
      check_health $PORT
    done

    ### Evaluate Model
    cd ../evaluation/
    python3 -m hyper_para_eval
    cd output

    if [ ! -d "$MODEL_FOLDER" ]; then
      mkdir "$MODEL_FOLDER"
    fi

    ls -p | grep -v / | xargs mv -t "$MODEL_FOLDER"
    cd $CURRENT_DIRECTORY

    ### Kill Container
    for ((i=0;i<NUMBER_OF_PARTITION;++i)); do
      PORT=$(( $START_PORT + $i))
      stop_container $PORT
    done

  fi
done
