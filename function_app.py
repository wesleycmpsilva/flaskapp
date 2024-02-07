import azure.functions as func
import logging
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

url_aurora = [
    {'sys_name': 'GAP', 'client': '100', 'url': 'https://solman.ab-inbev.com', 'alias': 'https://solman.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
    {'sys_name': 'GCP', 'client': '100', 'url': 'http://spgbpgtsa001.one.ofc.loc:8000', 'alias': 'https://slt.aurora.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
    {'sys_name': 'GWP', 'client': '200', 'url': 'http://spgbpsbwa001.one.ofc.loc:8000', 'alias': 'https://bw.aurora.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
    {'sys_name': 'S4P', 'client': '100', 'url': 'http://spstpss4a001.one.ofc.loc:8000', 'alias': 'https://s4.stout.aurora.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
    {'sys_name': 'S7P', 'client': '100', 'url': 'http://spstptdfa001.one.ofc.loc:8000', 'alias': 'https://tdf.stout.aurora.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
    {'sys_name': 'S9P', 'client': '100', 'url': 'https://sigga.stout.aurora.ab-inbev.com', 'alias': 'https://sigga.stout.aurora.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
    {'sys_name': 'STP', 'client': '100', 'url': 'http://spstptmsa001.one.ofc.loc:8000', 'alias': 'https://tm.stout.aurora.ab-inbev.com', 'akvkey': 'AURORA_PASSWORD'},
]

def https_call(item):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    count_success = 0
    output = "" # Initialize an empty string to accumulate messages

    # Loop through each URL and make a request with its corresponding password
    url = item['url']
    user = item['username']
    passwordKey = item['akvkey']
    ssl = item['ssl']
    
    password = os.environ[passwordKey] 
    auth = HTTPBasicAuth(username=user, password=password)

    try:
        response = requests.get(service_url, headers=headers, auth=auth, verify=ssl, timeout=5)
        output += f"{response.status_code} for {url}\n"
        output += response.text[:150] + "\n"

    except Exception as e:
        output += "{Erro by calling " + url + "}\n"

    return output

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
    #elif action == 1:
    #    output = sql_vm(req_body)

    return func.HttpResponse(
            output + "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )