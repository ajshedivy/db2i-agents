import os
from dotenv import load_dotenv, find_dotenv
from mapepire_python import connect

def test_mapepire():
    load_dotenv(find_dotenv())
    connection_details = {
        "host": os.getenv("HOST"),
        "user": os.getenv("DB_USER"),
        "port": os.getenv("PORT", 8075),
        "password": os.getenv("PASSWORD"),
        "ignoreUnauthorized": os.getenv("IGNORE_UNAUTHORIZED", True),
    }
    
    with connect(connection_details) as conn:
        with conn.execute('SELECT * FROM SAMPLE.EMPLOYEE') as cursor:
            if cursor.has_results:
                print(cursor.fetchone())
                
                
if __name__ == "__main__":
    test_mapepire()