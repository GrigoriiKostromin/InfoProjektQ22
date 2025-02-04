import tcod as libtcod
from input_handlers import handle_keys

def main():
    # Bildschirmgröße
    screen_width = 80
    screen_height = 50

    #Spielerposition
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    #importieren von assests (bilder)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    #Erzeugen der Konsole
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    
    #Keine Ahnung
    con = libtcod.console_new(screen_width, screen_height)

    #Variablen, die mit dem Input verbunden sind
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    #Spielschleife. Schleife läuft bis Fenster geschlossen ist
    while not libtcod.console_is_window_closed():
        #Input wird überprüft
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        #Spieler wird bei jeder Ändeung der Koordianten erzeugt
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()

        #Vorheriger Spieler wird gelöscht
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)
        
        #Es wir die Methode handle_keys aus input_handlers aufgerufen. An diese Methode wird die Inputvariable key weiter gegeben
        action = handle_keys(key)
        #Die einzelen Variablen aus input_handlers werden hier mit lokalen Variablen in Verbindung gesetzt
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        #Bewegung des Spielers
        if move:
            dx, dy = move
            player_x += dx
            player_y += dy
         
        #Fenster schließen
        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

#Es wird nur die main Funktion ausgeführt
if __name__ == '__main__':
    main()