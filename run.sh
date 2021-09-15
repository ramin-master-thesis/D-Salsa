#!/bin/bash

#!/bin/bash
PARTITION_COUNT=${1:-2}
START_PORT=${2:-5001}
PARTITION_METHOD=${3:-"murmur2"}


for ((i = 0; i < PARTITION_COUNT; ++i)); do
# shellcheck disable=SC2046
docker run --rm -d -p "$START_PORT":5000 -v $(pwd)/data:/app/data raminqaf/salsa:1.4 python -m server.app --content-index --partition-method "$PARTITION_METHOD" --partition-number "$i"
START_PORT=$((START_PORT+1))
done
