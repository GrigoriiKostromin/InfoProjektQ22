import tcod as libtcod


def handle_keys(key):
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

    if key.vk == libtcod.KEY_F11:
        # F11: Bildschrimgröße maximal
        return {'fullscreen': True}

    if key.vk == libtcod.KEY_F12:
        return {'fov_on': False}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Spiel beenden
        return {'exit': True}

    # Keine Taste wurde gedrückt
    return {}