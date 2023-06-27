import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from CreateSQLData import Networks
import getpass

class RetrieveSQLData:
    __metaclass__ = abc.ABCMeta

    def __init__(self, config_path):
        """ base class for SQL Data Retrieval

        Args:
            config_path (str): path to configuration file
        """
        config = configparser.ConfigParser()
        config.read(config_path)

        sql_address = str(config['sql']['address'])
        sql_user    = 'root' # getpass.getuser()
        sql_pswd    = getpass.getpass(prompt='password: ')
        sql_db      = str(config['sql']['db_name'])
        sql_port    = str(config['sql']['port'])
        
        sql_pswd = urllib.parse.quote(sql_pswd.encode('utf8'))

        self.url = 'mysql+pymysql://' + sql_user + ':' + sql_pswd + '@' + sql_address +\
                ':' + sql_port + '/' + sql_db + '?charset=utf8mb4&binary_prefix=true'


    def get_data(self):
        """
        """
        name = 'test_name'
        networks = session.query(Networks).filter_by(NETWORK_ID=name)
        network_list = []
        for network in networks:
            network_list += [str(network)]

    def write_data(self):
        """
        """

    def delete_networks(self):
        """
        """
        with session_scope(self.uri) as session:
              session.query('Networks').delete('fetch')
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


