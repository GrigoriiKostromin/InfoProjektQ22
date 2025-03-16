import os

import shelve


def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('savegame.dat', 'n') as data_file: # Man kreiert eine Datei wo die Listen, die Orte wo die Gegner usw. sind gespeichert werden, was dann beim starten geladen wird
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state

def load_game():

    if not os.path.isfile('savegame.dat'): # Wenn es noch keine Datei gibt, dann kann nichts geladen werden
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as data_file: # Wenn es die Datei gibt, wird es geladen und für die Listen, Variablen usw. alles eingesetzt
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state