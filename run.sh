#!/bin/bash

python databases.py start

# proof of principle:

# load data into sql/mongo databases
python create_synthetic_data.py

# read data from sql/mongo databases, write to disk
python retrieve_synthetic_data.py

# TODO: loop through time periods, write inputs to disk

# multifilter system will run on any data on disk
logging=0
n_filters=4
./multifilter_run $logging HarmonicModel $n_filters
 
python databases.py stop

