import json
import logging
import urllib.request
from .definitions import Entry

BASE_URL = 'http://localhost:8765'

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(BASE_URL, request_json)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        logging.error(response['error'])
    return response['result']


def is_anki_running():
    try:
        response = urllib.request.urlopen(urllib.request.Request(BASE_URL))
    except Exception as e:
        return False
    return True


def add_note(entry: Entry, deck='Web Development'):
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
    return invoke('addNote', **params)