import mysql.connector
from mysql.connector import Error
import configparser
import logging


logging.basicConfig(filename='../logs/sql-connector.log', format='%(asctime)s [%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s',
                    level=logging.DEBUG)


class SqlClient():

    def __init__(self, file_name, section_name):

        self.log = logging.getLogger(self.__class__.__name__)
        self.file_name = file_name
        self.section_name = section_name
        self.sql_client = None
        self.cursor = None

    def _get_option(self, section, option):

        config_parser = configparser.ConfigParser()
        config_parser.read(self.file_name)
        if config_parser.has_section(section) is False:
            self.log.warning('Section not found: %s', section)
            return None

        if config_parser.has_option(section, option) is False:
            self.log.warning(
                'Section %s does not have option: %s', section, option)
            return None
        return config_parser.get(section, option)

    def connect(self, to_database):

        username = self._get_option(self.section_name, 'username')
        password = self._get_option(self.section_name, 'password')
        host = self._get_option(self.section_name, 'host')
        port = self._get_option(self.section_name, 'port')
        database = self._get_option(self.section_name, 'database')

        try:
            if to_database:
                self.sql_client = mysql.connector.connect(
                    user=username, password=password, host=host, port=port, database=database, allow_local_infile=True)
                self.cursor = self.sql_client.cursor()
            else:
                self.sql_client = mysql.connector.connect(
                    user=username, password=password, host=host, port=port, allow_local_infile=True)
                self.cursor = self.sql_client.cursor()
            print('success')
            print(self.sql_client.is_connected())

        except Exception as e:
            self.log.error(e)
            self.sql_client = None

    def connect_db(self):
        port = self._get_option(self.section_name, 'port')

    def close_connection(self):
    	
        if self.sql_client is not None:
            try:
                self.sql_client.close()
                print('Connection is closed')
            except Exception as e:
                self.log.error(e)

    def execute(self, query):
        if self.sql_client is not None:
            try:
                self.cursor.execute(query)
                print('Query executed')
            except Error as e:
                self.log.error(e)
                self.connection = None
