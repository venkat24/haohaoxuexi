import json
import asyncio
import aiohttp

from cards import AnkiCard

DefaultHost = 'http://localhost:8765'

class AnkiClient():
    def __init__(self, deckname, hostname=DefaultHost):
        self.hostname = hostname
        self.deckname = deckname

    # Given an Anki card, create it on ANKI in the given deck
    async def createCard(self, card: AnkiCard):
        note = {
            "deckName": self.deckname,
            "modelName": "Basic",
            "fields": {
                "Front": card.front,
                "Back": card.back
            },
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck"
            }
        }

        return await self._execute('addNote', note=note)
    
    # Get a list of card IDs already existing in the current deck
    async def getCards(self):
        return await self._execute('findNotes', query=f"deck:{self.deckname}")
    
    # Execute an AnkiConnect operation
    async def _execute(self, action, **params):
        async with aiohttp.ClientSession() as session:
            requestJson = json.dumps(self._getRequestObject(action, **params)).encode('utf-8')
            async with session.get(self.hostname, data=requestJson) as responseHandler:
                response = json.loads(await responseHandler.text())
                if len(response) != 2:
                    raise Exception('response has an unexpected number of fields')
                if 'error' not in response:
                    raise Exception('response is missing required error field')
                if 'result' not in response:
                    raise Exception('response is missing required result field')
                if response['error'] is not None:
                    raise Exception(response['error'])
                return response['result']

    # Build the request object
    def _getRequestObject(self, action, **params):
        return { 'action': action, 'params': params, 'version': 6 }