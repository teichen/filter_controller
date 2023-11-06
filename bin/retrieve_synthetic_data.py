import getpass
from datetime import datetime
from RetrieveSQLData import RetrieveSQLData
from RetrieveMongoData import RetrieveMongoData

config_path = './data/inputs.ini'

def start_sessions():
    """
    """
    user = getpass.getuser()
    config_paths = [config_path, '/Users/' + str(user) + '/.mysql.ini']
    device_retriever = RetrieveSQLData(config_paths)

    measurement_retriever = RetrieveMongoData(config_path)
    
    return device_retriever, measurement_retriever

def close_sessions(device_retriever, measurement_retriever):
    """
    """
    device_retriever.close_session()

def retrieve_device_data(device_retriever):
    """
    """
    device_list = device_retriever.get_data() # e.g. [<Devices('test_name')>]

def retrieve_measurement_data(measurement_retriever):
    """ TODO
    """
    pass

if __name__ == '__main__':
    device_retriever, measurement_retriever = start_sessions()
    retrieve_device_data(device_retriever)
    retrieve_measurement_data(measurement_retriever)
    close_sessions(device_retriever, measurement_retriever)


