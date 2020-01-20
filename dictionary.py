import json

def displayDictionaryDetail():
    print(json.dumps(readDict(), sort_keys=True, indent=4))

def enterNewKeyword():
    newKey = input(' => Enter new Keyword for Scraping : ')
    dictionary = readDict()
    dictionary['search_key'] = newKey
    dictionary['next_page'] = 1
    dictionary['next_page'] = ''
    writeDict(dictionary)

def enterNewFilter():
    newFilter = str(input(' => Enter new Filter : '))
    dictionary = readDict()
    dictionary['filters'].append(newFilter)
    writeDict(dictionary)

def deleteFilter():
    deleteFilter = str(input(' => Enter new Filter : '))
    dictionary = readDict()
    dictionary['filters'].remove(deleteFilter)
    writeDict(dictionary)


def readDict():
    with open('dictionary_details.json', 'r') as fh:
        dictionary = json.load(fh)

    return dictionary

def writeDict(dictionary):
    with open('dictionary_details.json', 'w') as fh:
        json.dump(dictionary, fh)
