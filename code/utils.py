import os
import requests
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.exc import ProgrammingError


def check_table_exist(db_conn, table_name, table_type='BASE TABLE', table_schema='public'):
    sql = f'''SELECT * FROM
        information_schema.tables
    WHERE
    table_schema = '{table_schema}' AND
    table_type = '{table_type}' and
    table_name  = '{table_name}';
        '''
    return db_conn.execute(sql).fetchall()


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
    view_sql = '''CREATE VIEW  country_info as
    select wc.id, wc."iso2Code", wc.name, rc."name.common", rc."name.official",
        rc."unMember", rc."altSpellings", rc.landlocked, rc.population, rc.timezones,
        rc."car.side", rc."flags.png", rc."flags.svg",
        wc.longitude, wc.latitude, wc."region.id", wc."region.iso2code", wc."region.value",
        rc.region, rc.continents, rc."maps.googleMaps", rc."maps.openStreetMaps",
        wc."incomeLevel.id", wc."incomeLevel.iso2code", wc."incomeLevel.value",
        wc."lendingType.id", wc."lendingType.iso2code", wc."lendingType.value",
        rc."startOfWeek"
    from world_country wc, rest_country rc
    where wc."iso2Code" = rc.cca2 and wc.id = rc.cca3  ;
                '''
    db_conn.execute(view_sql)


def create_user(db_conn, username, password):
    check_user_sql = f'''select * from pg_user where usename = '{username}'; '''
    if not db_conn.execute(check_user_sql).fetchall():
        user_sql = f'''create user {username} password '{password}';
  GRANT CONNECT on DATABASE homex to {username};
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {username}; '''
        db_conn.execute(user_sql)

