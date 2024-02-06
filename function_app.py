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

def get_auth_headers(item, system_name):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    count_success = 0
    output = ""  # Initialize an empty string to accumulate messages

    # Loop through each URL and make a request with its corresponding password
    url = item['url']
    alias = item['alias']
    passwordKey = item['akvkey']
    client = item['client']

    service_url = url + f"/sap/opu/odata/AB4/GRC_CTE_OD_SEC01_APP_SRV_01/ControlDetailSet?sap-client={client}&sap-language=EN&saml2=disabled&$format=json"
    service_alias = alias + f"/sap/opu/odata/AB4/GRC_CTE_OD_SEC01_APP_SRV_01/ControlDetailSet?sap-client={client}&sap-language=EN&saml2=disabled&$format=json"

    user = 'SYS_MICSAUTO'
    password = os.environ[passwordKey] 
    auth = HTTPBasicAuth(username=user, password=password)

    exception_bool = False
    try:
        response = requests.get(service_url, headers=headers, auth=auth, verify=True, timeout=5)
        output += f"{response.status_code} for {url}\n"
        output += response.text[:150] + "\n"
        response = requests.get(service_url, headers=headers, auth=auth, verify=False, timeout=5)
        output += f"{response.status_code} for {url}\n"
        output += response.text[:150] + "\n"

        exception_bool = True
    except Exception as e:
        output += f"Error for {url}: {str(e)[0:75]}\n"

    try:
        response = requests.get(service_alias, headers=headers, auth=auth, verify=True, timeout=5)
        output += f"{response.status_code} for {alias}\n"
        output += response.text[:150] + "\n"
        response = requests.get(service_alias, headers=headers, auth=auth, verify=False, timeout=5)
        output += f"{response.status_code} for {alias}\n"
        output += response.text[:150] + "\n"

        exception_bool = True
    except Exception as e:
        output += f"Error for {alias}: {str(e)[0:75]}\n"
        output += "{Erro by calling " + url + "}\n"

    if exception_bool:
        count_success += 1
    output += "\n\n"

    return output

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

    try:
        pos = int(pos)
        if pos == -1:
            return func.HttpResponse(f"You are calling the request {pos}")
        else pos >= 0:
            output = get_auth_headers(url_aurora[pos])

            return func.HttpResponse(
                output + "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
                status_code=200
            )
    except Exception as e:
        return func.HttpResponse(f"An error had ocurred!")
