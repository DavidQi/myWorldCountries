import os
import requests
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.exc import ProgrammingError


def get_conn_string():
    if load_dotenv():
        postgre_info = (os.getenv('POSTGRES_USERNAME'),
                        os.getenv('POSTGRES_PASSWORD'),
                        os.getenv('POSTGRES_HOST'),
                        os.getenv('POSTGRES_PORT'),
                        os.getenv('POSTGRES_DATABASE'))
        if not all(postgre_info):
            raise Exception('Credential not exist!')
    else:
        raise Exception('Module dotenv not installed!')

    return 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(*postgre_info)


def load_countries_to_table(db_conn, url, table_name):
    level = 1
    try:
        r = requests.get(url).json()
        if 'worldbank' in url:
            r = r[1]
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    while level <= 5:
        try:
            df = pd.json_normalize(r, max_level=level)
            df.to_sql(f'{table_name}_raw', db_conn, if_exists='replace')
            df.dropna(axis=1).to_sql(table_name, db_conn, if_exists='replace')
            break
        except (psycopg2.ProgrammingError, ProgrammingError) as e:
            level += 1


def create_country_view(db_conn):
    with open('sql/create_views.sql', 'r') as fd:
        db_conn.execute(fd.read())
    with open('sql/create_user.sql', 'r') as fd:
        db_conn.execute(fd.read())
