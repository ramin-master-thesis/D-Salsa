#!/bin/bash

#############Partition Data && Create left/right index#######################
python -m partitioner.partition single && python -m graph.index single
python -m partitioner.partition modulo && python -m graph.index modulo
python -m partitioner.partition murmur2 && python -m graph.index murmur2
