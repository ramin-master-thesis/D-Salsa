#!/bin/bash

trap _ctrl_c INT

_ctrl_c() {
  echo "** graceful shutdown"
  curl http://localhost:5001/shutdown
  curl http://localhost:5003/shutdown
  curl http://localhost:5002/shutdown
  curl http://localhost:5005/shutdown
  curl http://localhost:5004/shutdown
  curl http://localhost:5006/shutdown
  curl http://localhost:5007/shutdown
  printf "\n"
}

### single_partition
python3 -m server.app --partition-method single_partition --port 5001 &

### murmur2
python -m server.app --partition-method murmur2 --partition-number 0 --port 5002 &
python -m server.app --partition-method murmur2 --partition-number 1 --port 5003 &

### StarSpace
python -m server.app --partition-method StarSpace --partition-number 0 --port 5004 &
python -m server.app --partition-method StarSpace --partition-number 1 --port 5005