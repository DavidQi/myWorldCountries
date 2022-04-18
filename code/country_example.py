import requests
import pandas as pd
from sqlalchemy import create_engine
from utils import get_conn_string, load_countries_to_table, create_country_view


base_url = 'http://localhost:5000'


def get_income():
    response = requests.get(base_url + '/report/income')
    print(response.text)


def get_unmembers():
    response = requests.get(base_url + '/report/unmembers')
    print(response.text)


def get_timezones():
    params = {'timezones': "+4,+5"}
    response = requests.get(base_url+'/report/timezones', headers='', params=params, timeout=5)
    print(response.text)


def get_tz():
    conn_string = get_conn_string()
    sql = ''' select id, name, timezones from country_info
where timezones like '%%UTC-04%%' and timezones like '%%UTC-05%%';
    '''
    db_conn = create_engine(conn_string).connect()
    results = pd.read_sql_query(sql, db_conn)
    print(results)


if __name__ == '__main__':
    get_income()
    get_unmembers()
    get_timezones()
    get_tz()
