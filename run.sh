#!/bin/bash

trap _ctrl_c INT

_ctrl_c() {
  echo "** graceful shutdown"
  curl http://localhost:5003/shutdown
  curl http://localhost:5002/shutdown
  printf "\n"
}

python -m server.app --partition-method modulo --partition-number 0 --port 5002 &
python -m server.app --partition-method modulo --partition-number 1 --port 5003