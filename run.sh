#!/bin/bash

python databases.py start

# proof of principle:
# load data into sql/mongo databases
python data/CreateMongoData.py

# read data from sql/mongo databases
# TODO: loop through time periods, write inputs to disk
# i.e. python data/RetrieveMongoData.py t0 t1
python data/RetrieveMongoData.py

./multifilter_run 0 HarmonicModel 4
 
# TODO: run the multi-filter controller for this time period [t0, t1]

python databases.py stop

