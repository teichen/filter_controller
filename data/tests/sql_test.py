import sys
sys.path.insert(1, '../')

from sqlalchemy import text
from CreateSQLData import CreateSQLData, Networks

config_path = '../inputs.ini'
sql_db = CreateSQLData(config_path)
sql_db.add_networks()

with sql_db.session_scope() as session:
    name = 'test_name'
    networks = session.query(Networks).filter_by(NETWORK_ID=name)
    for network in networks:
        print(network)

# clear table
sql_db.delete_tables()

