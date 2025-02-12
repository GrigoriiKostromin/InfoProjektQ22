import tcod as libtcod


def handle_keys(key):
    #Tasten zur Spielersteuerung. Hinter "move" sieht man, welche Koordiante veändert wird. Die erste Koordinate ist immer x
    if key.vk == libtcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'move': (1, 0)}

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