from functions import api_functions as f
from requests.auth import HTTPBasicAuth


class TTS:
    def __init__(self, name, guid, region_id):
        self.name = name
        self.guid = guid
        self.region = region_id
        self.api_key = f.get_resource_key(self.guid)
        self.url = "https://api." + self.region + ".text-to-speech.watson.cloud.ibm.com/instances/" + guid

    def get_voices(self):
        r_voices = f.API_CALL(
            method="GET",
            url=self.url + "/v1/voices",
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
        )

        return r_voices[0]
