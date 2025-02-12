from map_objects.rectangle import Rect
from map_objects.tile import Tile
from random import randint # Später für die Raumerstellung 

from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        #Dimensionen des Levels aus engine.py
        self.width = width
        self.height = height
        #?
        self.tiles = self.initialize_tiles()


    def initialize_tiles(self):
        #Tiles ist Klasse, in welcher zustände von Kacheln defeniert sind. Diese können hier später festgelegt werden
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)] # Quasi der ganze Bereich des Bildschirms


       
        # Test Wandkreation 
        """
        #Blockierte Kacheln = Wand. Koordinateten von Wänden müssen manuell angegeben werden 
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True """

        return tiles
    
    # Test Raumkreation
    """ 
    def make_map(self): # Zwei Räume und Tunnel testweise erstellen
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        # Hier wird ein Raum mithilfe der rect methode die wir in rectangle.py festgelegt haben erstellt
        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23) """
    

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):

        rooms = [] # Eine Liste in der alle Räume aufgeführt werden
        num_rooms = 0 # Wird später +1 addiert, wenn ein neuer Raum erstellt wird

        for r in range(max_rooms):
            # Zufällige Weite und Höhe wird festgelegt für den Raum
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Zufällige Koordinaten für den Startpunkt oben links, und innerhalb dass 
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # die generierten Werte werden in die Rect Methode eingegeben
            new_room = Rect(x, y, w, h)

            # Methode, die checkt ob die Räume sich überschneiden, wird gecalled und wenn sie sich überschneiden, dann wird der Vorgang abgebrochen 
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # Hier gibt es keine Überschneidungen

                # Neuer Raum wird kreiert 
                self.create_room(new_room)

                # Mit der Methode werden die Koordinaten berechnet
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # Der Spieler wird in den erst erstellten raum (mit num_rooms == 0 gecheckt) eingesetzt
                    player.x = new_x
                    player.y = new_y
                else:
                    # Neu erstellte Räume werden generiert und verbunden

                    # Koordinaten werden gespiechert
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # Entscheidung welcher Raum als Startraum verwendet wird.
                    if randint(0, 1) == 1:
                        # Verbinden
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room): #Sorgt quasi dafür dass innerhalb von dem in Rect festgelegten Rechteck es für den Spieler begehbar ist und er es auch sehen kann
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y): 
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False