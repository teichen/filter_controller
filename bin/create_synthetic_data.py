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
    """ create table of carriers which provide measurements
    """
    devices = {'test_name': 1575.42}

    device_creator.add_devices(devices)

def create_measurement_data(measurement_creator):
    """ create database of measurement data
    """
    carrier_name  = 'test_name'
    carrier_phase = 0.5 # cycles
    transmission_time  = datetime(2005, 6, 1, 0, 0)
    prn_code = [int(prn_element) for prn_element in np.array(np.floor(0.5 + random.rand(1023)))]

    measurements = [{'carrier_name': carrier_name, 'carrier_phase': carrier_phase, 
        'transmission_time': transmission_time, 'prn_code': prn_code}]

    measurement_creator.create_measurements(measurements)

if __name__ == '__main__':
    device_creator, measurement_creator = start_sessions()
    create_device_data(device_creator)
    create_measurement_data(measurement_creator)
    close_sessions(device_creator, measurement_creator)
