import tcod as libtcod

from game_states import GameStates


def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)

    return {}



def handle_player_turn_keys(key):
    key_char = chr(key.c)
    #Tasten zur Spielersteuerung. Hinter "move" sieht man, welche Koordiante veändert wird. Die erste Koordinate ist immer x
    """if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}"""
    
    if key.vk == libtcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'x':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':

        return {'move': (1, 0)}     
    elif key_char == 'q':
        return {'move': (-1, -1)}   # diagonal links vorne
    elif key_char == 'e':
        return {'move': (1, -1)}    # diagonal rechts vorne
    elif key_char == 'y':
        return {'move': (-1, 1)}    # diagonal links hinten
    elif key_char == 'c':
        return {'move': (1, 1)}     # diagonal links hinten

    if key_char == 'g':
        return {'pickup': True}

    elif key_char == 's':
        return {'show_inventory': True}

    elif key_char == 'l':
        return {'drop_inventory': True}

    if key.vk == libtcod.KEY_F11:
        # F11: Bildschrimgröße maximal
        return {'fullscreen': True}

    if key.vk == libtcod.KEY_F12:
        return {'fov_on': False}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Spiel beenden
        return {'exit': True}
    
    #Dungeon lvl aufsteigen
    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}

    # Keine Taste wurde gedrückt
    return {}

#Dies ist, um wenn man etwas ausgewählt, es mit ESC zu beenden
def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}


def handle_inventory_keys(key):
    index = key.c - ord('a') # ord ist ein Weg um Tasteninputs in einen Index umzuwandeln. Also a ist beispielsweise 0 und b ist dann 1, usw. usw.

    if index >= 0:
        return {'inventory_index': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

def handle_main_menu(key): # Hier ganz einfach die Inputs für das Startmenü
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    if key.vk == libtcod.KEY_F11:
        # F11: Bildschrimgröße maximal
        return {'fullscreen': True}

    return {}

def handle_end_menu(key): # Hier ganz einfach die Inputs für das Startmenü
    key_char = chr(key.c)

    if key_char == 'a' or  key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    if key.vk == libtcod.KEY_F11:
        # F11: Bildschrimgröße maximal
        return {'fullscreen': True}

    return {}

#Funktion, um Mausinput zu triggern
def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}