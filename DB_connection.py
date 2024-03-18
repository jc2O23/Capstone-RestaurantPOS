from configparser import ConfigParser
from mysql.connector import Error, MySQLConnection
from git_hub import json_github
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))


def create_db_connection(db):
    db_config = read_db_config(db)

    try:
        print("Attempting Connection to Database...")
        connection = MySQLConnection(**db_config)
        if connection.is_connected():
            print("Connection established")
        else:
            print("Connection failed")

    except Error as err:
        print("Connection failed ")
        print(f"Error: '{err}'")
        quit()

    return connection

def read_db_config(section):
    # Read database config file and return a dictionary object

    filename='./data/DB_config.ini'
    # parse and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{} not found in the {} file'.format(section, filename))

    return db
