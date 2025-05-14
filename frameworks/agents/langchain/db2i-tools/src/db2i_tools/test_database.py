import unittest
from unittest.mock import patch, MagicMock
import pytest
from db2i_tools.database import Db2iDatabase
import os
from dotenv import load_dotenv

def load_connection():
    load_dotenv()
    connection_details = {
        "host": os.getenv("HOST"),
        "user": os.getenv("DB_USER"),
        "port": os.getenv("PORT", 8075),
        "password": os.getenv("PASSWORD"),
        "schema": os.getenv("SCHEMA"),
    }
    return connection_details


config = load_connection()
SCHEMA = 'SAMPLE'

def test_get_all_table_names():
    db = Db2iDatabase(schema=SCHEMA, server_config=config)
    result = db._get_all_table_names(config["schema"])
    print(result)
    
def test_simple_execute():
    db = Db2iDatabase(schema=SCHEMA, server_config=config)
    sql = "SELECT * FROM SAMPLE.EMPLOYEE"
    result = db._execute(sql)
    print(result)
    
def test_get_table_definition():
    db = Db2iDatabase(schema=SCHEMA, server_config=config)
    result = db._get_table_definition("EMPLOYEES")
    print(result)
    
def test_table_info():
    db = Db2iDatabase(schema=SCHEMA, server_config=config)
    result = db.get_table_info(["EMP_PHOTO"])
    print(result)
    
def test_all_table_info():
    db = Db2iDatabase(schema=SCHEMA, server_config=config)
    result = db.get_table_info()
    print(result)
    
def test_simple_run():
    db = Db2iDatabase(schema=SCHEMA, server_config=config)
    result = db.run("SELECT * FROM SAMPLE.EMPLOYEE")
    print(result)
        
def main():
    # test_get_all_table_names()
    # test_simple_execute()
    # test_get_table_definition()
    test_table_info()
    # test_simple_run()
    # test_all_table_info()
    
if __name__ == "__main__":
    main() 