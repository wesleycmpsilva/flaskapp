import azure.functions as func
import logging
import requests
from pprint import pprint
from requests.auth import HTTPBasicAuth
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

url_aurora = [
    {'sys_name': 'GAP', 'client': '100', 'url': 'https://solman.ab-inbev.com', 'alias': 'https://solman.ab-inbev.com', 'akvkey': 'sysmicsautopass-gap100'},
    {'sys_name': 'GCP', 'client': '100', 'url': 'http://spgbpgtsa001.one.ofc.loc:8000', 'alias': 'https://slt.aurora.ab-inbev.com', 'akvkey': 'sysmicsautopass-gcp100'},
    {'sys_name': 'GWP', 'client': '200', 'url': 'http://spgbpsbwa001.one.ofc.loc:8000', 'alias': 'https://bw.aurora.ab-inbev.com', 'akvkey': 'sysmicsautopass-gwp200'},
    {'sys_name': 'S4P', 'client': '100', 'url': 'http://spstpss4a001.one.ofc.loc:8000', 'alias': 'https://s4.stout.aurora.ab-inbev.com', 'akvkey': 'sysmicsautopass-s4p100'},
    {'sys_name': 'S7P', 'client': '100', 'url': 'http://spstptdfa001.one.ofc.loc:8000', 'alias': 'https://tdf.stout.aurora.ab-inbev.com', 'akvkey': 'sysmicsautopass-s7p100'},
    {'sys_name': 'S9P', 'client': '100', 'url': 'https://sigga.stout.aurora.ab-inbev.com', 'alias': 'https://sigga.stout.aurora.ab-inbev.com', 'akvkey': 'sysmicsautopass-s9p100'},
    {'sys_name': 'STP', 'client': '100', 'url': 'http://spstptmsa001.one.ofc.loc:8000', 'alias': 'https://tm.stout.aurora.ab-inbev.com', 'akvkey': 'sysmicsautopass-stp100'},
]

@app.route(route="http_adb_middleware")
def http_adb_middleware(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pos = req.params.get('pos')
    if not pos:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            pos = req_body.get('pos')

    if not pos:
        return func.HttpResponse(f"You are not calling any request")
    if pos == -1:
        return func.HttpResponse(f"You are calling the request {pos}")
    else:
    
        output += "\n\n"

        return func.HttpResponse(
             output + "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )