import getpass
from datetime import datetime
from CreateSQLData import CreateSQLData, Devices
from CreateMongoData import CreateMongoData

config_path = './data/inputs.ini'

def start_sessions():
    """
    """
    user = getpass.getuser()
    config_paths = [config_path, '/Users/' + str(user) + '/.mysql.ini']

    device_creator = CreateSQLData(config_paths)

    measurement_creator = CreateMongoData(config_path)

    return device_creator, measurement_creator

def close_sessions(device_creator, measurement_creator):
    """
    """
    # clear table
    device_creator.delete_tables()
    device_creator.close_session()

    measurement_creator.close_session()

def create_device_data(device_creator):
    """ create table of devices which provide measurements
    """
    device_names  = ['test_name']

    device_creator.add_devices(device_names)

def create_measurement_data(measurement_creator):
    """ create database of measurement data
    """
    measurement_name  = 'test_name'
    measurement_value = 1.0
    measurement_time  = datetime(2005, 6, 1, 0, 0)

    measurements = [{'measurement_name': measurement_name, 'measurement_value': measurement_value, 
            'measurement_time': measurement_time}]

    measurement_creator.create_measurements(measurements)

if __name__ == '__main__':
    device_creator, measurement_creator = start_sessions()
    create_device_data(device_creator)
    create_measurement_data(measurement_creator)
    close_sessions(device_creator, measurement_creator)
