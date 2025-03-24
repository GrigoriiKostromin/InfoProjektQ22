import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.equipment import Equipment
from components.equippable import Equippable

from entity import Entity

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder
from equipment_slots import EquipmentSlots


def get_constants(): # Hier die Daten die wir in Engine festlegten "ausgeklammert" in dieser Funktion
    window_title = 'Roguelike'

    #Bildschirmgr��e (im kleinen Zustand)
    screen_width = 80
    screen_height = 50

    #UI Panel
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    #Log f�r die Nachrichten. Parameter
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    #gr��e der Karte/Levels
    map_width = 80
    map_height = 43

    # Variablen f�r bestimmte Raumtypen die erstellt werden
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    #Variablen f�r die begrenzte sicht 
    fov_algorithm = 0       #tcod Sichtfeld Algorithmus.
    fov_light_walls = True  #Wenn der Parameter True ist, werden die W�nde "beleuchtet"
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

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants

equipment_component = Equipment()

hp = 15000
defense = 0
power = 1
def get_game_variables(constants):
    fighter_component = Fighter(hp, defense, power) # fighter_component gibt den Spieler Werte, die n�tig sind, um zu k�mpfen
    inventory_component = Inventory(26) # Hier wird festgelegt, dass der Spieler 26 Pl�tze im Inventar hat
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, equipment=equipment_component) # Erzeugen eines Spieler aus der Entity Klasse 
    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, max_hp_bonus=0, power_bonus=6, defense_bonus=0)
    stick = Entity(0, 0, '/', libtcod.grey, 'Stock', equippable=equippable_component)
    player.inventory.add_item(stick)
    player.equipment.toggle_equip(stick)

    equippable_component = Equippable(EquipmentSlots.OFF_HAND, max_hp_bonus=0, power_bonus=0, defense_bonus=0)
    fassdeckel = Entity(0, 0, '[', libtcod.grey, 'Fassdeckel', equippable=equippable_component)
    player.inventory.add_item(fassdeckel)
    player.equipment.toggle_equip(fassdeckel)

    equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, max_hp_bonus=0, power_bonus=0, defense_bonus=0)
    norm_ring = Entity(0, 0, 'o', libtcod.grey, 'Gewoehnlicher Ring', equippable=equippable_component)
    player.inventory.add_item(norm_ring)
    player.equipment.toggle_equip(norm_ring)

    equippable_component = Equippable(EquipmentSlots.ARMOR, max_hp_bonus=10, power_bonus=0, defense_bonus=0)
    gewandt = Entity(0, 0, 'M', libtcod.grey, 'Seidegewandt', equippable=equippable_component)
    player.inventory.add_item(gewandt)
    player.equipment.toggle_equip(gewandt)



    


    

   

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities) # Es werden die Methoden in Gamemap gecalled mit den zuf�llig festgelegten Variablen

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state