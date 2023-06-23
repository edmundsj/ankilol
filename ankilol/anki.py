import json
import logging
import urllib.request
from ankilol.definitions import Entry



class AnkiConnect:

    def __init__(self, version=6, base_url='http://localhost:8765'):
        self.version = version
        self.base_url = base_url

    def _request(self, action, **params):
        return {'action': action, 'params': params, 'version': self.version}

    def _invoke(self, action, **params):
        request_json = json.dumps(self._request(action, **params)).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request(self.base_url, request_json)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            logging.error(response['error'])
        return response['result']

    def is_running(self):
        try:
            response = urllib.request.urlopen(urllib.request.Request(self.base_url))
        except Exception as e:
            return False
        return True

    def sync(self):
        return self._invoke('sync')

    def add_note(self, entry: Entry, deck='Web Development'):
        params = {
            'note': {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {
                    "Front": entry.question,
                    "Back": entry.answer
                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": deck,
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                },
                "tags": [
                ],
            }
        }
        logging.info(f'Adding note {entry.question}')
        return self._invoke('addNote', **params)
