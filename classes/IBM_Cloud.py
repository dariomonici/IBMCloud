from functions import api_functions as f
import constants as k
import json

class IBM_Cloud:
    def __init__(self):
        f = open('secrets.json', "r")
        secrets = json.loads(f.read())
        self.name = "IBM Cloud"
        self.api_key = secrets[self.name]['api_key']

    def update_values(self, api_key):
        self.api_key = api_key

    def get_token(self):
        r_token = f.API_CALL(method="POST",
                             url='https://iam.cloud.ibm.com/identity/token',
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             body={
                                 "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                                 "apikey": self.api_key
                             })

        return r_token[0]['access_token']

    def get_resource_instances(self):
        r_resources = f.API_CALL(method="GET",
                                url='https://resource-controller.cloud.ibm.com/v2/resource_instances',
                                headers={'authorization': 'Bearer ' + self.get_token()}
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

    def get_resource_instances_by_type(self, t):
        r_resources = f.API_CALL(method="GET",
                                 url='https://resource-controller.cloud.ibm.com/v2/resource_instances',
                                 headers={'authorization': 'Bearer ' + self.get_token()}
                                 )
        list_instances = {}

        for r in r_resources[0]['resources']:
            if t in r['crn']:
                list_instances.setdefault(r['name'], {'guid': r['guid'], 'name': r['name'], 'crn': r['crn'], 'region_id': r['region_id']})

        return list_instances

    def get_resource_instance(self, guid):
        r_resource = f.API_CALL(method="GET",
                                url='https://resource-controller.cloud.ibm.com/v2/resource_instances/'+guid,
                                headers={'authorization': 'Bearer ' + self.get_token()}
                                 )

        return r_resource[0]

    def get_resource_key(self):
        r_key = f.API_CALL(method="GET",
                                url="https://resource-controller.cloud.ibm.com/v2/resource_keys/90e3b10f-803e-4b5d-9d86-abca677865be",
                                headers={'authorization': 'Bearer ' + self.get_token()}
                                 )

        return r_key[0]
