from functions import api_functions as f
from requests.auth import HTTPBasicAuth
import json

class WLT:
    def __init__(self, name, guid, region_id):
        self.name = name
        self.guid = guid
        self.region = region_id
        self.api_key = f.get_resource_key(self.guid)
        self.url = "https://api." + self.region + ".language-translator.watson.cloud.ibm.com/instances/" + guid
        self.version = "2018-05-01"

    def translate(self, input_data, lang_model):
        r_translate = f.API_CALL(
            method="POST",
            url=self.url + "/v3/translate?version=" + self.version,
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
            req_data={
                "text": input_data,
                "model_id": lang_model
            },
            json=True
        )

        return r_translate[0]['translations'][0]['translation']

    def get_languages(self):
        r_languages = f.API_CALL(
            method="GET",
            url=self.url + "/v3/languages?version=" + self.version,
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
        )

        return r_languages[0]

    def get_models(self):
        r_models = f.API_CALL(
            method="GET",
            url=self.url + "/v3/models?version=" + self.version,
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
        )

        return r_models[0]
