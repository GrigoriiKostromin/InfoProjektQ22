import tcod as libtcod
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all
from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from game_messages import Message


def main():
    constants = get_constants() # Nutzt die Funktion in "initialize_new_game.py" um die ganzen Variablen zu laden

    #Position von Objekten, wie Spieler, Npcs, Items, etc
    """player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)     VIELLEICHT FÜR SPÄTER DAS??
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.red)
    entities = [npc, player]"""

    #importieren von assests (bilder)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    #Erzeugen eines Fensters
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)


    #erstellen einer Konsole
    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    #Erstellen einer weitern Konsole
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background.png') # Hintergrundbild laden (bisher Platzhalter)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed(): 
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], # Hier wird der Bildschirm erstellt
                      constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'Kein Spiel zum laden!!', 67, constants['screen_width'], constants['screen_height']) # Dieses Main wird nur gestartet, wenn es kein vorheriges Spiel gab

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants) # Standarddaten werden geladen hier
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game: 
                try:
                    player, entities, game_map, message_log, game_state = load_game() # Datenübertragung aus der Datei
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

            show_main_menu = True
    


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants): # Fast alles was zuvor in MAIN drin war
    #Wenn die Map generiert wird der Bereich, in dem man sehen kann "aktiviert"
    fov_recompute = True

    #Die Map wird als Parameter für die Erezeugung des Sichtfeldes weitergegeben
    fov_map = initialize_fov(game_map)
    fov_on = True

    #Variablen, die mit dem Input verbunden sind
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    previous_game_state = game_state

    #Das ist nötig um ein Ziel füt Items festzulegen. Default: es kein Ziel (nötig füt Zauber)
    targeting_item = None

    #Spielschleife. Schleife läuft bis Fenster geschlossen ist
    while not libtcod.console_is_window_closed():
        #Input wird überprüft
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        #Es werden Parameter 
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        #Rednerfunktion wird gecalled
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)
        
           
        fov_recompute = False
        libtcod.console_flush()

        #Letzer Schritt wird gecleared
        clear_all(con, entities)
        


        #Es wir die Methode handle_keys aus input_handlers aufgerufen. An diese Methode wird die Inputvariable key weiter gegeben
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)
        
        #Die einzelen Variablen aus input_handlers werden hier mit lokalen Variablen in Verbindung gesetzt
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        fov_on = action.get('fov_on')

        #Mausinput
        
        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        #Eine Liste zum Speichern der Ergebnisse der Aktionen des Spielers während seines Zuges
        player_turn_results = []

        #Bewegung des Spielers
        if move and game_state == GameStates.PLAYERS_TURN: # Hier wird getestet, ob der Spieler an der Reihe ist. (Also ob die Gegner sich schon bewegt haben)
            dx, dy = move
            destination_x = player.x + dx # Für das Prüfen wo der Spieler sich hinbewegen möchte, wird das hier berechnet, damit es gleich sofort an die "get_blocking_entities_at_location" übergeben werden kann
            destination_y = player.y + dy
            #Methode aus entity.py für die Bewegung. Keine Bewgung möglich, wenn eine Kachel blockiert ist. Also eine Wand existiert
            if not game_map.is_blocked(destination_x, destination_y): # Wenn "False" returned wird, dann wird das hier ausgeführt 
                target = get_blocking_entities_at_location(entities, destination_x, destination_y) # Hier wird dann die Entity ausgegeben

                if target: # Wenn du gegen eine Entity rennst, dann geschieht das 
                    # Wenn es ein Ziel gibt, greift der Spieler. Speichert Ergebnisse des Angriffs
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy) # Wenn du in niemanden reinrennst, wird einfach die Bewegung wie immer durchgeführt
                    #Diese Variable muss True sein, damit sich das Sichtfeld ändert. Diese Variable ist nur True, wenn die Koordinaten des Spielers sich änder.
                    fov_recompute = True 

                game_state = GameStates.ENEMY_TURN # JETZT ist der Gegner an der Reihe
         
        elif pickup and game_state == GameStates.PLAYERS_TURN: # Sodass man nur aufheben kann wenn der Spieler an der Reihe ist
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y: # Wenn die an der selben Stelle sind, dann:
                    pickup_results = player.inventory.add_item(entity) # Hier die Methode abgerufen mit dem Item (entity) mit dem man interagiert
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('Es gibt nichts zum Aufheben.', libtcod.yellow))

        #Inventar öffnen (benutzen)
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        #Inventar öffnen (fallen lassen)
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map)) # Hier wird dann die use methode gecalled, sodass auch das passiert, was mit dem Item passieren soll.

            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))


        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                #Wemm sich der Spieler über den Treppen befindet und enter drückt, wird eine neues lvl generiert
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        #Hier wird das Ziel festgelegt
        if game_state == GameStates.TARGETING:
            #Mit Linksclick wird ein Ziel ausgewählt. Also deren x- und y-Koordinaten
            if left_click:
                target_x, target_y = left_click

                #Item mit Target wird benutzt
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            #Wenn Rechtsklick, wird das Auswählen abgebrochen
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})



        #Fenster schließen, wenn es geöffnet war. Das Auswählen eines Zieles wird abgebrochen
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)

                return True



        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


        # Verarbeitet alle Ergebnisse aus dem Zug des Spielers wie Kampfmeldungen 
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')

            if message:
                message_log.add_message(message)

            if dead_entity:
                #Wenn Spieler stirbt, wird kill_player gecalled
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                #Wenn Gegner stirbt, wird kill_monster gecalled
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added) # Hier wird das Item von der Map genommen was man aufgehoben hat.

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN # das Konsumieren/verwenden eines Gegenstandes verbraucht den Zug des Spielers

            #Item fallen lassen
            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN
            

            #Wen wir ein Item benutzen, welches ein Ziel braucht, gehen wir zum Spielerzug, damit sich das Inventar nicht nochmal öffnet
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                message_log.add_message(targeting_item.item.targeting_message)
            
            #Das Ziel wird abgebrochen
            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            


        if game_state == GameStates.ENEMY_TURN: # Hier werden die einzelnen Gegner durchgegangen und es wird geschaut was sie alle machen.
            for entity in entities: 
                if entity.ai: # Hierbei wird natürlich der Spieler ausgelassen.
                    #Die KI mit dem Spieler und der Umgebung interagieren lassen.
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    # Verarbeiten von der Ergebnisse der Aktionen des Feindes.
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)
                        
                        
                        if dead_entity:
                            #Wenn Spieler stirbt, wird kill_player gecalled
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            #Wenn Gegner stirbt, wird kill_monster gecalled
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)
                            
                            #Wenn Spieler stirbt bewegen sich die Gegner nicht mehr
                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    #Wenn Spieler stirbt bewegen sich die Gegner nicht mehr
                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN

#Es wird nur die main Funktion ausgeführt
if __name__ == '__main__':
    main()