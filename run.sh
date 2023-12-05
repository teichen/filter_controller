#!/bin/bash

python databases.py start

# proof of principle:

# load data into sql/mongo databases
python create_synthetic_data.py

# read data from sql/mongo databases, write to disk
python retrieve_synthetic_data.py

# run the GNSS application
python gnss_application.py

python databases.py stop

