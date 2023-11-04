# filter_controller
controller for multiple Kalman filters

# to start sql/mongo databases
python databases.py start

# load data into sql/mongo databases
python data/CreateMongoData.py

# read data from sql/mongo databases
# TODO: loop through time periods, write inputs to disk
# i.e. python data/RetrieveMongoData.py t0 t1
python data/RetrieveMongoData.py

# to stop sql/mongo databases
python databases.py stop

