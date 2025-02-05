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
        #Tiles ist Klasse, in welcher zusünde von Kacheln defeniert sind. Diese können hier später festgelegt werden
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]


       
        
        """
        #Blockierte Kacheln = Wand. Koordinateten von Wänden müssen manuell angegeben werden 
        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True """

        return tiles
   
    def make_map(self): # Zwei Räume und Tunnel testweise erstellen
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        # Hier wird ein Raum mithilfe der rect methode die wir in rectangle.py festgelegt haben erstellt
        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23)

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