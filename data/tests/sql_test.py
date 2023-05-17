import sys
sys.path.insert(1, '../')

from CreateSQLData import CreateSQLData

config_path = '../inputs.ini'
sql_db = CreateSQLData(config_path)
sql_db.add_networks()
