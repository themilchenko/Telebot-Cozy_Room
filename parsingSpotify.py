import pandas as pd
import json

def top_artists(char_size):
    result = ''
    jsonData = pd.read_json('json_files/top_artists_' + char_size + '.json')
    for idx, item in enumerate(jsonData['items']):
        if (idx + 1) < 10:
            result += str(idx + 1) + '.   ' + item['name'] + ';\n     Genre: ' + item['genres'][0] + '.\n\n'
        else:
            result += str(idx + 1) + '.  ' + item['name'] + ';\n     Genre: ' + item['genres'][0] +'.\n'
    return result

def top_tracks(char_size):
    result = ''
    jsonData = pd.read_json('json_files/top_tracks_' + char_size + '.json')
    for idx, item in enumerate(jsonData['items']):
        # track = item['album']
        if (idx + 1) < 10:
            result += str(idx + 1) + '.  ' + item['name'] + " – " + item['album']['artists'][0]['name'] + '\n'
        else:
            result += str(idx + 1) + '. ' + item['name'] + " – " + item['album']['artists'][0]['name'] + '\n'
    return result

def greeting():
    jsonData = json.load(open('json_files/me.json'))
    res = "Hi, " + str(jsonData['display_name']) + "!\nYou've got " + str(jsonData['followers']['total']) + ' followers.'
    return res
