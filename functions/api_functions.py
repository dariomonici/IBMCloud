import requests
from requests.auth import HTTPBasicAuth
import constants as k

requests.packages.urllib3.disable_warnings()

def API_CALL(method, url, headers, json=True, verify=False, req_data=None, auth=None, body=None):
    r = requests.request(method, url, auth=auth, data=body, headers=headers, verify=verify, json=req_data)
    sc = r.status_code
    if json == True:
        return r.json(), sc
    else:
        return r, sc

def get_token():
    r_token = API_CALL(method="POST",
                             url='https://iam.cloud.ibm.com/identity/token',
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             body={
                                 "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                                 "apikey": k.API_KEY
                             })

    return r_token[0]['access_token']

def get_resource_instances():
    r_resources = API_CALL(method="GET",
                                url='https://resource-controller.cloud.ibm.com/v2/resource_instances',
                                headers={'authorization': 'Bearer ' + get_token()}
                                 )

    list_resources = {}
    for s in k.services_to_check:
        list_resources[s] = []

    for r in r_resources[0]['resources']:
        for s in k.services_to_check:
            if s in r['crn']:
                list_resources[s].append(
                    {'guid': r['guid'], 'name': r['name'], 'crn': r['crn'], 'region_id': r['region_id']})

    return list_resources

def get_resource_instances_by_type(t):
    r_resources = API_CALL(method="GET",
                                 url='https://resource-controller.cloud.ibm.com/v2/resource_instances',
                                 headers={'authorization': 'Bearer ' + get_token()}
                                 )
    list_instances = {}

    for r in r_resources[0]['resources']:
        if t in r['crn']:
            list_instances.setdefault(r['name'], {'guid': r['guid'], 'name': r['name'], 'crn': r['crn'], 'region_id': r['region_id']})

    return list_instances

def get_resource_instance(guid):
    r_resource = API_CALL(method="GET",
                                url='https://resource-controller.cloud.ibm.com/v2/resource_instances/ '+ guid,
                                headers={'authorization': 'Bearer ' + get_token()}
                                 )

    return r_resource[0]

def get_resource_key(guid):
    r_key = API_CALL(method="GET",
                    url="https://resource-controller.cloud.ibm.com/v2/resource_instances/" + guid + "/resource_keys",
                    headers={'authorization': 'Bearer ' + get_token()}
                    )

    return r_key[0]['resources'][0]['credentials']['apikey']