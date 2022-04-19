import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify, request
from flask_caching import Cache
from utils import get_conn_string, load_countries_to_table, create_country_view, check_table_exist, create_user

app = Flask(__name__)
cache = Cache(app)


@app.route('/')
def welcome():
    return "Welcome to Homex!"


# http://localhost:5000/report/income
@app.route('/report/income')
@cache.cached(timeout=604800)  # cache set to 1 week in seconds
def income():
    results = ''
    sql = '''select
        region, "incomeLevel.id", count(id)
        country_num, sum(population)
        population
        from country_info group
        by
        region, "incomeLevel.id";'''
    conn_string = get_conn_string()
    try:
        db_conn = create_engine(conn_string).connect()
        results = pd.read_sql(sql, db_conn).to_json()
    except Exception as e:
        return {"error": str(e)}
    return {"results": results}


# http://localhost:5000/report/unmembers
@app.route('/report/unmembers')
@cache.cached(timeout=604800)  # cache set to 1 week in seconds
def unmebers():
    results = ''
    sql = '''select id, name, "name.common", landlocked
        from country_info where "unMember" is True ;'''
    try:
        conn_string = get_conn_string()
        db_conn = create_engine(conn_string).connect()
        results = pd.read_sql(sql, db_conn).to_json()
    except Exception as e:
        return {"error": str(e)}
    return {"results": results}


# http://localhost:5000/report/timezones?timezones=-4,-5
# http://localhost:5000/report/timezones?timezones=%2B5,%2B6
@app.route('/report/timezones', methods=["GET"])
@cache.cached(timeout=604800)  # cache set to 1 week in seconds
def timezones():
    results = ''
    timezones = request.args.get('timezones').split(',')
    if all([t.startswith('-') or t.startswith('+') for t in timezones]):
        timezon_str = [f"timezones like '%%UTC{t.zfill(3)}%%'" for t in timezones]
        sql = f'''select id, name, timezones from country_info
            where {' and '.join(timezon_str)};'''
        print(sql)
        conn_string = get_conn_string()
        try:
            db_conn = create_engine(conn_string).connect()
            results = pd.read_sql(sql, db_conn).to_json()
        except Exception as e:
            return{"error": str(e)}
    return {"results": results}


# http://localhost:5000/buildview
@app.route('/buildview')
def create_view():
    conn_string = get_conn_string()
    db_conn = create_engine(conn_string).connect()

    if check_table_exist(db_conn, 'country_info', 'VIEW'):
        return "DB View has already been built!"

    rest_url = 'https://restcountries.com/v3.1/all'
    wb_url = 'https://api.worldbank.org/v2/country?per_page=300&format=json'

    load_countries_to_table(db_conn, rest_url, 'rest_country')
    load_countries_to_table(db_conn, wb_url, 'world_country')
    create_country_view(db_conn)
    create_user(db_conn, 'analyst_team', '12345')
    return "DB View has been built!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
