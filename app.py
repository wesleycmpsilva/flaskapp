from flask import Flask, request, jsonify
import logging
import requests
from requests.auth import HTTPBasicAuth
import os
import pyodbc

app = Flask(__name__)

def str_to_bool(s):
    s = s.lower()
    return s in ['true', 't', 'yes', 'y', '1']

def https_call(item):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    response_data = {}

    url = item['url']
    user = item['username']
    passwordKey = item['akvkey']
    ssl = item['ssl']
    route = item['route']

    ssl = str_to_bool(ssl)
    password = os.environ[passwordKey] 
    auth = HTTPBasicAuth(username=user, password=password)

    try:
        response = requests.get(url + route, headers=headers, auth=auth, verify=ssl, timeout=5)
        response_data['status_code'] = response.status_code
        response_data['response'] = response.text
    except Exception as e:
        response_data['error'] = str(e)

    return response_data


def sql_vm(item):
    ip = item['ip']
    database = item['database']
    user = item['username']
    passwordKey = item['akvkey']
    password = os.environ[passwordKey]

    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={ip};DATABASE={database};UID={user};PWD={password};Authentication=ActiveDirectoryPassword;TrustServerCertificate=YES;'

    query_results = []
    SQL_QUERY = """SELECT 1"""

    try:
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        for row in rows:
            query_results.append(dict(zip(columns, row)))
    except Exception as e:
        query_results.append({'error': str(e)})

    return query_results

@app.route('/http_adb_middleware', methods=['POST'])
def http_adb_middleware():
    try:
        req_body = request.get_json()
    except ValueError:
        return jsonify("Invalid request format"), 400

    action = req_body.get('action')
    details = req_body.get('details')

    if action == 0:
        output = https_call(details)
    elif action == 1:
        output = sql_vm(details)
    else:
        return jsonify("Invalid action"), 400

    return jsonify(output), 200

if __name__ == '__main__':
    app.run()
