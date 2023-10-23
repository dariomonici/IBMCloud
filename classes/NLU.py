from functions import api_functions as f
from requests.auth import HTTPBasicAuth
import json

class NLU:
    def __init__(self, name, guid, region_id):
        self.name = name
        self.guid = guid
        self.region = region_id
        self.api_key = f.get_resource_key(self.guid)
        self.url = "https://api." + self.region + ".natural-language-understanding.watson.cloud.ibm.com/instances/" + guid
        self.version = "2022-04-07"

    def categories(self, input_data, input_type, num_categories):
        r_categories = f.API_CALL(
            method="POST",
            url=self.url + "/v1/analyze?version=" + self.version,
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
            req_data={
                input_type: input_data,
                "features": {"categories": {"limit": num_categories}}
            },
            json=True
        )

        return r_categories[0]['categories']
    
    def classifications(self, input_data, input_type):
        r_classifications = f.API_CALL(
            method="POST",
            url=self.url + "/v1/analyze?version=" + self.version,
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
            req_data={
                input_type: input_data,
                "features": {"classifications": {"model":"tone-classifications-en-v1"}}
            },
            json=True
        )

        if 'classifications' in r_classifications[0]:
            return r_classifications[0]['classifications']
        elif 'error' in r_classifications[0]:
            return r_classifications[0]['error']
        

    def get_models(self):
        r_models = f.API_CALL(
            method="GET",
            url=self.url + "/v1/models?version=" + self.version,
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
        )

        return r_models[0]
