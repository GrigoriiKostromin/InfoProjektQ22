import tcod as libtcod
from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap




def main():
    #Bildschirmgröße (im kleinen Zustand)
    screen_width = 80
    screen_height = 50
    #größe der Karte/Levels
    map_width = 80
    map_height = 45

# Variablen für bestimmte Raumtypen die erstellt werden
    room_max_size = 10  
    room_min_size = 6
    max_rooms = 30

    #Farben der Karte (Styling)
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }

    #Position von Objekten, wie Spieler, Npcs, Items, etc
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]


    #importieren von assests (bilder)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    #Erzeugen der Konsole
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)


    #Keine Ahnung. Muss schauen, was .console_new macht
    con = libtcod.console_new(screen_width, screen_height)
    
    #Karte wird erzeugt
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player) # Es werden die Methoden in Gamemap gecalled mit den zufällig festgelegten Variablen

    #Variablen, die mit dem Input verbunden sind
    key = libtcod.Key()
    mouse = libtcod.Mouse()



    #Spielschleife. Schleife läuft bis Fenster geschlossen ist
    while not libtcod.console_is_window_closed():
        #Input wird überprüft
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        #Spieler wird bei jeder Ändeung der Koordianten erzeugt
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        libtcod.console_flush()

        #Letzer Schritt wird gecleared
        clear_all(con, entities)


        #Es wir die Methode handle_keys aus input_handlers aufgerufen. An diese Methode wird die Inputvariable key weiter gegeben
        action = handle_keys(key)
        #Die einzelen Variablen aus input_handlers werden hier mit lokalen Variablen in Verbindung gesetzt
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')


        #Bewegung des Spielers
        if move:
            dx, dy = move
            #Methode aus entity.py für die Bewegung. Keine Bewgung möglich, wenn eine Kachel blockiert ist. Also eine Wand existiert
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
         
        #Fenster schließen
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

#Es wird nur die main Funktion ausgeführt
if __name__ == '__main__':
    main()