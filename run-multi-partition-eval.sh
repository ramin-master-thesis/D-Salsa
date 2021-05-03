#!/bin/bash

trap _ctrl_c INT

_ctrl_c() {
  echo "** graceful shutdown"
  prune_partitions
  printf "\n"
}

deploy_container() {
  PORT=$1
  PARTITION_METHOD=$2
  PARTITION_NUMBER=$3
  docker run --rm -d -p "$PORT":5000 -v $(pwd)/data:/app/data raminqaf/salsa:1.2 python -m server.app --partition-method "$PARTITION_METHOD" --partition-number "$PARTITION_NUMBER"
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

deploy_partitions() {
  PARTITION_METHOD=$1

  ### Start Server
  for ((i = 0; i < NUMBER_OF_PARTITION; ++i)); do
    PORT=$(($START_PORT + $i))
    deploy_container $PORT $PARTITION_METHOD $i
  done

  for ((i = 0; i < NUMBER_OF_PARTITION; ++i)); do
    PORT=$(($START_PORT + $i))
    check_health $PORT
  done
}

run_evaluation_suit() {
  PARTITION_METHOD=$1
  ### Evaluate evaluate
  cd ../evaluation/
  CONFIG_FILE="$PARTITION_METHOD"-evaluation.yaml
  python3 -m main ./configs/$CONFIG_FILE
  cd output

  if [ ! -d "$PARTITION_METHOD" ]; then
    mkdir "$PARTITION_METHOD"
  fi
  ls -p | grep -v / | xargs mv -t "$PARTITION_METHOD"
  cd $CURRENT_DIRECTORY
}

prune_partitions() {
  ## Kill Container
  for ((i = 0; i < NUMBER_OF_PARTITION; ++i)); do
    PORT=$(($START_PORT + $i))
    stop_container $PORT
  done
}

if [ -z "$1" ]; then
  echo "No arguments supplied. Please pass the number of partitions 2, 4, 8,..."
  exit 1
fi
NUMBER_OF_PARTITION=$1
START_PORT=5000
CURRENT_DIRECTORY=$(pwd)

### Partition and Index Data
MODEL="lr_0.01_dim_300_dropoutRHS_0.8_normalizeText_True"
python3 -m partitioner.main "single" \
& python3 -m partitioner.main "murmur2" -n "$NUMBER_OF_PARTITION" \
& python3 -m partitioner.main "star-space" -n "$NUMBER_OF_PARTITION" -m $MODEL


#### single_partition
deploy_container $START_PORT "single_partition" "0"
check_health $START_PORT
run_evaluation_suit "single"
stop_container $START_PORT
sleep 10

### murmur2
deploy_partitions "murmur2"
run_evaluation_suit "murmur2"
prune_partitions
sleep 15

### star-space
deploy_partitions "star-space"
run_evaluation_suit "star-space"
prune_partitions
