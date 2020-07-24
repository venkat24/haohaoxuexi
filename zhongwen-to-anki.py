import os, sys, time
import json
import urllib.request

DeckName = '汉字/生词'
AnkiHost = 'http://localhost:8765'

def deleteFile(fileName):
    os.remove(fileName)
    print(f"Deleted {fileName}")

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(AnkiHost, requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def createCard(front, back):
    note = {
        "deckName": DeckName,
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back
        },
        "options": {
            "allowDuplicate": False,
            "duplicateScope": "deck"
        }
    }
    result = invoke('addNote', note=note)

def getCards():
    return invoke('findNotes', query="deck:current")

def convertFromZhongwenExport(zhongwenFileName):
    entries = []
    outFileName = f"anki{int(time.time())}.txt"

    with open(zhongwenFileName, 'r') as infile:
        for row in infile:
            item = tuple(row.split('\t')[:-1])
            entries.append({
                "front": item[0],
                "back": f"({item[2]}) {item[3]}"
            })

    with open(outFileName, 'w') as outfile:
        for entry in entries:
            line = "\t".join([entry["front"], f"{entry['back']}\n"])
            outfile.write(line)

    return entries

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Specify an input file.")
        exit(1)

    inFileName = sys.argv[1]
    entries = convertFromZhongwenExport(inFileName)

    print(f"Converted {len(entries)} cards to ANKI format...")

    print(f"Starting export of {len(entries)} new cards to ANKI...")
    print(f"Found {len(getCards())} cards already in deck {DeckName} on ANKI...")

    for i, entry in enumerate(entries):
        try:
            createCard(entry["front"], entry["back"])
        except:
            print(f"Duplicate card {i} of {len(entries)} ({entry['front']}), skipping...")
            continue

        print(f"Added card {i} of {len(entries)} ({entry['front']})...")
        
    print(f"Task finished, {len(getCards())} cards now in deck {DeckName} on ANKI...")
    
    deleteFile(inFileName)
    print(f"Deleted {inFileName}...")
    print(f"Completed! 去好好学习 :)")
