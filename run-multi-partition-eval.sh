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
  docker run --rm -d -p "$PORT":5000 -v $(pwd)/data:/app/data raminqaf/salsa:1.3 python -m server.app \
  --partition-method "$PARTITION_METHOD" \
  --partition-number "$PARTITION_NUMBER" \
  --no-content-index
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
  START_PORT=${2:-5000}

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
  PARTITION_FOLDER="$NUMBER_OF_PARTITION"_partitions
  CONFIG_FILE="$PARTITION_METHOD"-evaluation.yaml
  python3 -m main ./configs/$PARTITION_FOLDER/$CONFIG_FILE
  cd output

  if [ ! -d "$PARTITION_METHOD" ]; then
    mkdir "$PARTITION_METHOD"
  fi
  ls -p | grep -v / | xargs mv -t "$PARTITION_METHOD"
  cd $CURRENT_DIRECTORY
}

prune_partitions() {
  ## Kill Container
  START_PORT=${1:-5000}
  for ((i = 0; i < NUMBER_OF_PARTITION; ++i)); do
    PORT=$(($START_PORT + $i))
    stop_container $PORT
  done
}

if [ -z "$1" ]; then
  echo "No arguments supplied. Please pass the number of partitions 2, 4, 8,..."
  exit 1
fi
NUMBER_OF_PARTITION=$1 # First argument determines the number of partitions
SHOULD_PARTITION=${2:-false} # Second argument by default is set to false, determines if the partitioning should be done from scratch or just read from disk
SHOULD_INCLUDE_SINGLE=${3:-true} # Third argument by default is set to true, determines if the single partition should be calculated from scratch
START_PORT=5000
CURRENT_DIRECTORY=$(pwd)

### Partition and Index Data
if $SHOULD_PARTITION ; then
    printf 'Partitioning the data\n'
    MODEL="lr_0.01_dim_300_dropoutRHS_0.8_normalizeText_True"
    python3 -m partitioner.main "single" \
    & python3 -m partitioner.main "murmur2" -n "$NUMBER_OF_PARTITION" \
#    & python3 -m partitioner.main "star-space" -n "$NUMBER_OF_PARTITION" -m $MODEL
else
  printf 'Copying the partitions from the partitions folder'
  PARTITION_FOLDER="$NUMBER_OF_PARTITION"_partitions
  cp -r ../partitions/"$PARTITION_FOLDER"/* ./data/
fi


#### single_partition
if $SHOULD_INCLUDE_SINGLE ; then
  deploy_container $START_PORT "single_partition" "0"
  check_health $START_PORT
  run_evaluation_suit "single"
  stop_container $START_PORT
  sleep 10
fi

### murmur2
(
printf "starting murmur2"
deploy_partitions "murmur2" $START_PORT
run_evaluation_suit "murmur2"
prune_partitions $START_PORT
) &
#sleep 15

### star-space
#(
#printf "starting StarSpace"
#PORT=$(($START_PORT+$NUMBER_OF_PARTITION))
#deploy_partitions "star-space" $PORT
#run_evaluation_suit "star-space"
#prune_partitions $PORT
#)
