import azure.functions as func
import logging
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth
import os
import pyodbc

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def str_to_bool(s):
    # Convert the string to lowercase to make the function case-insensitive
    s = s.lower()
    if s in ['true', 't', 'yes', 'y', '1']:
        return True
    elif s in ['false', 'f', 'no', 'n', '0']:
        return False

def https_call(item):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    output = "" # Initialize an empty string to accumulate messages

    # Loop through each URL and make a request with its corresponding password
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
        output += f"{response.status_code} for {url}\n"
        output += response.text + "\n"

    except Exception as e:
        output += f"Erro {e} by calling + {url}{route} \n"

    return output

def sql_vm(item):

    ip = item['ip']
    database = item['database']
    user = item['username']
    passwordKey = item['akvkey']
    password = os.environ[passwordKey]

    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={ip};DATABASE={database};UID={user};PWD={password};Authentication=ActiveDirectoryPassword;TrustServerCertificate=YES;'
    
    results = ""


    return "IT'S ALL OK"

@app.route(route="http_adb_middleware")
def http_adb_middleware(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(f"You are not calling any request")

    action = req_body.get('action')
    details = req_body.get('details')

    if action == 0:
        output = https_call(details)
    elif action == 1:
        output = sql_vm(details)

    return func.HttpResponse(
            output + "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )