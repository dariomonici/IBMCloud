from functions import api_functions as f
from requests.auth import HTTPBasicAuth
import os

class TTS:
    def __init__(self, name, guid, region_id):
        self.name = name
        self.guid = guid
        self.region = region_id
        self.api_key = f.get_resource_key(self.guid)
        self.url = "https://api." + self.region + ".text-to-speech.watson.cloud.ibm.com/instances/" + guid

    def synthesize(self, text_to_synthesize):
        if os.path.exists(os.getcwd() + 'tts_audio.wav'):
            os.remove('data/tts/tts_audio.wav')

        r_synthesize, sc = f.API_CALL(
            method="POST",
            url=self.url + "/v1/synthesize",
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={'Content-Type': 'application/json',
                     'Accept': 'audio/wav'},
            req_data={'text': text_to_synthesize},
            json=False
        )

        with open('data/tts/tts_audio.wav', 'wb') as audio_file:
            audio_file.write(r_synthesize.content)

    def get_voices(self):
        r_voices = f.API_CALL(
            method="GET",
            url=self.url + "/v1/voices",
            auth=HTTPBasicAuth('apikey', self.api_key),
            headers={"Content-Type": "application/json"},
        )

        return r_voices[0]
