from map_objects.rectangle import Rect
from map_objects.tile import Tile
import tcod as libtcod
from random import randint
from render_functions import RenderOrder

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.equipment import EquipmentSlots
from components.equippable import Equippable

from entity import Entity
from game_messages import Message
from item_functions import heal, cast_lightning, cast_fireball

from map_objects.rectangle import Rect
from map_objects.tile import Tile
from components.stairs import Stairs

from random_utils import from_dungeon_level, random_choice_from_dict


class GameMap:
    def __init__(self, width, height , dungeon_level=1):
        #Dimensionen des Levels aus engine.py
        self.width = width
        self.height = height
        #?
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
        self.treasure_x = 0
        self.treasure_y = 0

    def initialize_tiles(self):
        #Tiles ist Klasse, in welcher zusünde von Kacheln defeniert sind. Diese können hier später festgelegt werden
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)] # Alle Kacheln auf den Bildschirm werden als Tiles festgelegt. 


       
        # WÄNDE DIE ZUM TEST ERSTELLT WURDEN !!!
        """
        #Blockierte Kacheln = Wand. Koordinateten von Wänden müssen manuell angegeben werden 
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True """

        return tiles
   
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities): # Zwei Räume und Tunnel testweise erstellen ||| Sonst so: def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, npc)
        """room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        # Hier wird ein Raum mithilfe der rect methode die wir in rectangle.py festgelegt haben erstellt
        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23)"""

        rooms = []
        num_rooms = 0
        
        #Die Koordinaten des am letzten genrierten Raumes
        center_of_last_room_x = None
        center_of_last_room_y = None
        
        
        

        for r in range(max_rooms):
            # Hier werden zufällige Werte für Werte für die Höhe und die Weite erstellt, die dann später in die Rect Funktion eingesetzt werden
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Hier wird der Generationsort (quasi die Kachel für das obere linke Eck) für den neu erstellten Raum ausgegeben
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Hier werden die vorherig generierten Werte in unsere Rect Funktion eingesetzt
            new_room = Rect(x, y, w, h)

            # Hier werden alle Räume (über die Liste "rooms") durchgegangen und mithilfe der intersect Methode geprüft ob sie sich schneiden, wenn sie es tun wird es beendet
            for other_room in rooms:
                if new_room.intersect(other_room) == True:
                    break

            else:
                # Hier geht es weiter, wenn nicht ge"break"ed wird und der Raum sich nicht mit den vorherig generierten Räumen überschneidet

                # Unser erstellter Raum wird mithilfe der create_room auf die Map gebracht
                self.create_room(new_room)
                # Hier werden einfach die Koordinten vom Mittelpunkt des neuerstellten Raumes berechnet, um sie später für das "platzieren" des Spielers verwendet werden
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y
                
                
              
                
                    
                #erster Raum
                if num_rooms == 0:
                    # Hier wird der Spieler im zuerst generierten Raum (num_rooms ist nur ganz am Anfang 0, direkt danach wird die Nummer immer +1 gemacht) platziert
                    player.x = new_x
                    player.y = new_y
                    
                    
                    
                
                else:
                    # Das gilt jetzt für alle Räume, die NICHT der erste sind. Hier werden jetzt die Räume mit den Tunneln verbunden (würde beim ersten keinen Sinnn ergeben, da der ja noch nichts hätte womit man ihn verbinden könnte)

                    # Wir nehmen die zentralen Koordinaten des gerade eben erstellten Raums und wir greifen auf vorherigen Raum mithilfe der Liste zu und verbinden den auch in der Mitte
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Hier wird quasi eine "Münze geworfen", ob wir zuerst einen horizontalen oder eine vertikalen Tunnel erstellenm 
                    if randint(0, 1) == 1:
                        # Zuerst einen Horizontalen, dann einen Vertikalen
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # Zuerst einen Vertikalen, dann einen Horizontalen
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                #Schatzraum
                if num_rooms == 1:
                    self.treasure_x = new_x
                    self.treasure_y = new_y
                # Pro Raum wird immer VIELLEICHT ein Mob platziert
                self.place_entities(new_room, entities) # Hier wird unsere Methode "Place Entities" gecalled, und die Werte übergeben. 

                # num_rooms wird 1 zugefügt, weil wir jetzt zum nächsten Raum kommen und der gerade eben erstellte Raum wird der Liste hinzugefügt
                rooms.append(new_room)
                num_rooms += 1

        #Es wird eine Treppe kreiert, welche ins mächte lvl führt
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):  #Sorgt quasi dafür dass innerhalb von dem in Rect festgelegten Rechteck es für den Spieler begehbar ist und er es auch sehen kann
        for x in range(room.x1 + 1, room.x2): # Hier wird quasi jede einzelne Kachel ausgezählt und in die "liste" x dann eingesetzt
            for y in range(room.y1 + 1, room.y2): # Hier das selbe mit all den y Werten
                self.tiles[x][y].blocked = False #Hier werden jetzt alle Kacheln die wir in der Liste x und der Liste y haben durchgegangen und die Variable blocked wird auf false gesetzt, sodass wir sie begehen können
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y): 
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [4, 9], [6, 13], [9, 17], [11, 22]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 3], [3, 13]], self.dungeon_level)
        # Hier wird eine zufällige Nummer generiert, wie viele Gegner auf der Karte auftauchen sollen
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {'troll':70 , 'ork': 20, 'spinne': 15, 'riese': 5} # Hier werden die Wahrscheinlichkeiten definiert
        item_chances = {'heiltrank': 70, 'blitzzauber': 10, 'feuerballzauber': 10} # Hier für Items

        #Eine Liste, in der die Wahrscheinlichkeiten im Bezug zum level geändert werden
        monster_chances = {
            'troll': 80,
            'ork': from_dungeon_level([[15, 3], [30, 5], [50, 7],[40, 13]], self.dungeon_level),
            'spinne': from_dungeon_level([[30, 2], [40, 5], [25, 9]], self.dungeon_level),
            'riese': from_dungeon_level([[5, 5], [10, 7], [15, 9], [20, 13], [30, 17], [40, 19]], self.dungeon_level)
        }
        
        #Eine Liste, in der die Wahrscheinlichkeiten im Bezug zum level geändert werden
        item_chances = {
            'heiltrank': from_dungeon_level([[35, 1], [0, 11]], self.dungeon_level),
            'grosser_heiltrank': from_dungeon_level([[35, 11]], self.dungeon_level),
            'blitzzauber': from_dungeon_level([[15, 4]], self.dungeon_level),
            'feuerballzauber': from_dungeon_level([[25, 6]], self.dungeon_level),
            'dolch': from_dungeon_level([[20, 1], [2, 5]], self.dungeon_level),
            'kurz_schwert': from_dungeon_level([[15, 4], [1, 11]], self.dungeon_level),
            'lang_schwert': from_dungeon_level([[10, 8], [1, 15]], self.dungeon_level),
            'gross_schwert': from_dungeon_level([[7, 14]], self.dungeon_level),
            'rund_schild': from_dungeon_level([[10, 1], [1, 10]], self.dungeon_level),
            'gross_schild': from_dungeon_level([[5, 10]], self.dungeon_level),
            

            
        }

        treasure_chances = {
            'ring_des_lebens_1': from_dungeon_level([[3, 1], [0, 9]], self.dungeon_level),
            'ring_des_schutzes_1': from_dungeon_level([[3, 1], [0, 9]], self.dungeon_level),
            'ring_des_schadens_1': from_dungeon_level([[3, 1,], [0, 9]], self.dungeon_level),
            'ring_des_lebens_2': from_dungeon_level([[30, 9], [0, 17]], self.dungeon_level),
            'ring_des_schutzes_2': from_dungeon_level([[30, 9], [0, 17]], self.dungeon_level),
            'ring_des_schadens_2': from_dungeon_level([[30, 9], [0, 17]], self.dungeon_level),
            'ring_des_lebens_3': from_dungeon_level([[31, 17]], self.dungeon_level),
            'ring_des_schutzes_3': from_dungeon_level([[31, 17]], self.dungeon_level),
            'ring_des_schadens_3': from_dungeon_level([[31, 17]], self.dungeon_level),
            'leder_robe': from_dungeon_level([[90, 1], [0, 9]], self.dungeon_level),
            'ketten_ruestung': from_dungeon_level([[10, 9], [0,17]], self.dungeon_level),
            'ritter_ruestung': from_dungeon_level([[7, 17]], self.dungeon_level),
            'der_ring_aus_den_legenden': from_dungeon_level([[1, 1]], self.dungeon_level),


        }
        if not any([entity for entity in entities if entity.x == self.treasure_x and entity.y == self.treasure_y]):
            treasure_choice = random_choice_from_dict(treasure_chances)
                        
                            
            if treasure_choice == 'ring_des_lebens_1':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, max_hp_bonus=20)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.violet, 'Ring des Lebens 1', equippable=equippable_component,)
                                entities.append(item)

            elif treasure_choice == 'ring_des_schutzes_1':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, defense_bonus=2)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.blue, 'Ring des Schutzes 1',equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_schadens_1':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, power_bonus=2)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.red, 'Ring des Schadens 1', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_lebens_2':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, max_hp_bonus=50)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.violet, 'Ring des Lebens 2', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_schutzes_2':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, defense_bonus=4)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.blue, 'Ring des Schutzes 2', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_schadens_2':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, power_bonus=5)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.red, 'Ring des Schadens 2', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_lebens_3':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, max_hp_bonus=300)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.violet, 'Ring des Lebens 3', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_schutzes_3':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, defense_bonus=7)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.blue, 'Ring des Schutzes 3', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ring_des_schadens_3':
                                equippable_component = Equippable(EquipmentSlots.SPECIAL_SLOT, power_bonus=15)
                                item = Entity(self.treasure_x, self.treasure_y, 'o', libtcod.red, 'Ring des Schadens 3', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'leder_robe':
                                equippable_component = Equippable(EquipmentSlots.ARMOR, power_bonus=1, max_hp_bonus=20, defense_bonus=1)
                                item = Entity(self.treasure_x, self.treasure_y, 'M', libtcod.darker_orange, 'Leder Robe', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ketten_ruestung':
                                equippable_component = Equippable(EquipmentSlots.ARMOR, power_bonus=3, max_hp_bonus=50, defense_bonus=5)
                                item = Entity(self.treasure_x, self.treasure_y, 'M', libtcod.darker_orange, 'Kettenruestung', equippable=equippable_component)
                                entities.append(item)

            elif treasure_choice == 'ritter_ruestung':
                                equippable_component = Equippable(EquipmentSlots.ARMOR, power_bonus=20, max_hp_bonus=100, defense_bonus=20)
                                item = Entity(self.treasure_x, self.treasure_y, 'M', libtcod.darker_orange, 'Ritterruestung', equippable=equippable_component)
                                entities.append(item)
            
            elif treasure_choice == 'der_ring_aus_den_legenden':
                                equippable_component = Equippable(EquipmentSlots.ARMOR, power_bonus=300, max_hp_bonus=0, defense_bonus=-1)
                                item = Entity(self.treasure_x, self.treasure_y, '+', libtcod.yellow, 'Ring Der Legenden', equippable=equippable_component)
                                entities.append(item)
        

        for i in range(number_of_monsters):
            # Zufällige Koordinaten von einem Raum der erstellt wurde
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances) 

                if monster_choice == 'ork': 
                    fighter_component = Fighter(hp=30, defense=1, power=15)#Kampfattribute, die mit der Entity Klasse in Verbindug stehen
                    ai_component = BasicMonster()   #AI, die "später" das autonome Bewegen der Gegner ermöglichen wird

                    monster = Entity(x, y, 'T', libtcod.darker_red, 'Ork', blocks=True, fighter=fighter_component,
                                     ai=ai_component) # Hier ein Troll. Ork bekommt eine AI und Kampfattribute
                    
                elif monster_choice == 'riese':
                    fighter_component = Fighter(hp=150, defense=5, power=70)#Kampfattribute, die mit der Entity Klasse in Verbindug stehen
                    ai_component = BasicMonster()   #AI, die "später" das autonome Bewegen der Gegner ermöglichen wird

                    monster = Entity(x, y, 'T', libtcod.darker_blue, 'Riese', blocks=True, fighter=fighter_component,
                                     ai=ai_component) # Hier ein Troll. Ork bekommt eine AI und Kampfattribute   
                    
                elif monster_choice == 'spinne':
                    fighter_component = Fighter(hp=1, defense=0, power=33)#Kampfattribute, die mit der Entity Klasse in Verbindug stehen
                    ai_component = BasicMonster()   #AI, die "später" das autonome Bewegen der Gegner ermöglichen wird

                    monster = Entity(x, y, 'o', libtcod.black, "Spinne", blocks=True, fighter=fighter_component,
                                        ai=ai_component) # Hier ein Troll. Ork bekommt eine AI und Kampfattribute
                    
                    
                else:
                    fighter_component = Fighter(hp=20, defense=0, power=6) #Kampfattribute, die mit der Entity Klasse in Verbindug stehen
                    ai_component = BasicMonster()   #AI, die "später" das autonome Bewegen der Gegner ermöglichen wird

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component) # Quasi ein Ork. Ork bekommt eine AI und Kampfattribute

                entities.append(monster)

        for i in range(number_of_items): # Hier der selbe Prozess wie bei dem platzieren von den Gegnern, hier nur mit den Gegenständen
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            

            if not any([entity for entity in entities if entity.x == x and entity.y == y]): # Wird platziert wenn keine bisher drin ist.
                item_choice = random_choice_from_dict(item_chances)
                

                if item_choice == 'blitzzauber':
                    item_component = Item(use_function=cast_lightning, damage=100, maximum_range=5)
                    item = Entity(x, y, '#', libtcod.yellow, 'Blitzzauber', render_order=RenderOrder.ITEM,
                                  item=item_component)
                    
                    

                elif item_choice == 'feuerballzauber':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Linksklicke die Kachel, auf welche der Feuerball landen soll. Rechtsklicke um den Zauber abzubrechen', libtcod.light_cyan),
                                          damage=25, radius=3)
                    item = Entity(x, y, '#', libtcod.red, 'Feuerballzauber', render_order=RenderOrder.ITEM,
                                  item=item_component)
                
                elif item_choice == 'dolch':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.darker_orange, 'Dolch', equippable=equippable_component)

                elif item_choice == 'kurz_schwert':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6)
                    item = Entity(x, y, '/', libtcod.darker_orange, 'Kurzschwert', equippable=equippable_component)

                elif item_choice == 'lang_schwert':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=12)
                    item = Entity(x, y, '/', libtcod.darker_orange, 'Langschwert', equippable=equippable_component)

                elif item_choice == 'gross_schwert':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=29)
                    item = Entity(x, y, '/', libtcod.darker_orange, 'Grossschwert', equippable=equippable_component)

                elif item_choice == 'rund_schild':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=2)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Rundschild', equippable=equippable_component)
                
                elif item_choice == 'gross_schild':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=6)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Grossschild', equippable=equippable_component)
                
                elif item_choice == 'grosser_heiltrank':
                    item_component = Item(use_function=heal, amount=100) # Wird zu Items hinzugefügt
                    item = Entity(x, y, '!', libtcod.violet, 'Großer Heiltrank', render_order=RenderOrder.ITEM,
                                item=item_component) # Hier bisher nur die Potion

                else:
                    item_component = Item(use_function=heal, amount=50) # Wird zu Items hinzugefügt
                    item = Entity(x, y, '!', libtcod.violet, 'Heiltrank', render_order=RenderOrder.ITEM,
                                item=item_component) # Hier bisher nur die Potion
                entities.append(item)
                

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]
        
        #Wenn ein neues Dungen lvl erreicht wird, wird eine neue Map kreiert und das mit den selben Parametern wie die vorherige Map
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        #Spieler wird um die hälfte seiner Leben geheilt
        player.fighter.heal(player.fighter.max_hp // 2)
        #Lognachricht
        message_log.add_message(Message('Du ruhst dich für einen Moment aus und erholst dich.', libtcod.light_violet))

        return entities
    
    def game_end(self):
        dungeon_level = self.dungeon_level
        if dungeon_level == 25:
            return True
        else:
            return False