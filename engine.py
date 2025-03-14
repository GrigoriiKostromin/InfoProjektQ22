import tcod as libtcod
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from render_functions import clear_all, render_all, RenderOrder
from map_objects.game_map import GameMap
from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from game_messages import Message, MessageLog


def main():
    #Bildschirmgröße (im kleinen Zustand)
    screen_width = 80
    screen_height = 50

    #UI Panel
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    	
    #Log für die Nachrichten. Parameter 
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    #größe der Karte/Levels
    map_width = 80
    map_height = 43

    # Variablen für bestimmte Raumtypen die erstellt werden
    room_max_size = 10  
    room_min_size = 6
    max_rooms = 30

    #Variablen für die begrenzte sicht 
    fov_algorithm = 0       #tcod Sichtfeld Algorithmus.
    fov_light_walls = True  #Wenn der Parameter True ist, werden die Wände "beleuchtet"
    fov_radius = 10         #Sichtradius

    max_monsters_per_room = 3
    max_items_per_room = 2

    #Farben der Karte (Styling)
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(16, 110, 41),  #Beleuchtete Wand
        'light_ground': libtcod.Color(116, 184, 134) #Beleuchteter Boden
    }

    #Position von Objekten, wie Spieler, Npcs, Items, etc
    """player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)     VIELLEICHT FÜR SPÄTER DAS??
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.red)
    entities = [npc, player]"""

    fighter_component = Fighter(hp=30, defense=2, power=5) # fighter_component gibt den Spieler Werte, die nötig sind, um zu kämpfen
    inventory_component = Inventory(26) # Hier wird festgelegt, dass der Spieler 26 Plätze im Inventar hat
    player = Entity(0, 0, '@', libtcod.white, 'Spieler', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component) # Erzeugen eines Spieler aus der Entity Klasse 
    entities = [player]

    #importieren von assests (bilder)
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    #Erzeugen eines Fensters
    libtcod.console_init_root(screen_width, screen_height, 'roguelike', False)


    #erstellen einer Konsole
    con = libtcod.console_new(screen_width, screen_height)
    #Erstellen einer weitern Konsole
    panel = libtcod.console_new(screen_width, panel_height)
    
    #Karte wird erzeugt
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room) # Es werden die Methoden in Gamemap gecalled mit den zufällig festgelegten Variablen
    
    #Wenn die Map generiert wird der Bereich, in dem man sehen kann "aktiviert"
    fov_recompute = True

    #Die Map wird als Parameter für die Erezeugung des Sichtfeldes weitergegeben
    fov_map = initialize_fov(game_map)
    fov_on = True

    #Den Nachrichtenlog verwenden
    message_log = MessageLog(message_x, message_width, message_height)

    #Variablen, die mit dem Input verbunden sind
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    #Spielschleife. Schleife läuft bis Fenster geschlossen ist
    while not libtcod.console_is_window_closed():
        #Input wird überprüft
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        #Es werden Parameter 
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        #Rednerfunktion wird gecalled
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width,
                   screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state)
        
           
        fov_recompute = False
        libtcod.console_flush()

        #Letzer Schritt wird gecleared
        clear_all(con, entities)
        


        #Es wir die Methode handle_keys aus input_handlers aufgerufen. An diese Methode wird die Inputvariable key weiter gegeben
        action = handle_keys(key, game_state)
        #Die einzelen Variablen aus input_handlers werden hier mit lokalen Variablen in Verbindung gesetzt
        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        fov_on = action.get('fov_on')

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

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

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



        #Fenster schließen
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
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

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN


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