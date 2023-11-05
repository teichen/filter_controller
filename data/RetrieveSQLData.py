import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import configparser
from contextlib import contextmanager
from CreateSQLData import Devices
import getpass
import urllib

class RetrieveSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config_paths):
        """ base class for SQL Data Retrieval

        Args:
            config_path (list): list of paths to configuration files
        """
        config = configparser.ConfigParser()
        config.read(config_paths)

        sql_address = str(config['sql']['address'])
        sql_user    = 'root' # getpass.getuser()
        sql_pswd    = str(config['sql']['password'])
        sql_db      = str(config['sql']['db_name'])
        sql_port    = str(config['sql']['port'])
        
        sql_pswd = urllib.parse.quote(sql_pswd.encode('utf8'))

        self.url = 'mysql+pymysql://' + sql_user + ':' + sql_pswd + '@' + sql_address +\
                ':' + sql_port + '/' + sql_db + '?charset=utf8mb4&binary_prefix=true'

        self.engine  = create_engine(self.url, pool_size=30, pool_recycle=3600)
        session_interface = sessionmaker(bind=self.engine)
        self.session = scoped_session(session_interface)()

    def get_data(self):
        """
        """
        name = 'test_name'
        devices = self.session.query(Devices).filter_by(NETWORK_ID=name)
        device_list = []
        for device in devices:
            device_list += [str(device)]

        return device_list

    def write_data(self):
        """
        """
        pass

    def delete_devices(self):
        """
        """
        with self.session_scope() as session:
              session.query(Devices).delete('fetch')
              session.commit()

    @contextmanager
    def session_scope(self):
        session = self.session
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def close_session(self):
        """ close SQL session
        """
        self.session.close()


