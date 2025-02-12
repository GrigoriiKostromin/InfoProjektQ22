from map_objects.rectangle import Rect
from map_objects.tile import Tile
from random import randint

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
   
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, npc): # Zwei Räume und Tunnel testweise erstellen
        """room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)
        # Hier wird ein Raum mithilfe der rect methode die wir in rectangle.py festgelegt haben erstellt
        self.create_room(room1)
        self.create_room(room2)
        self.create_h_tunnel(25, 40, 23)"""

        rooms = []
        num_rooms = 0

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
                (new2_x, new2_y) = new_room.center()
                
                if num_rooms == 0:
                    # Hier wird der Spieler im zuerst generierten Raum (num_rooms ist nur ganz am Anfang 0, direkt danach wird die Nummer immer +1 gemacht) platziert
                    player.x = new_x
                    player.y = new_y
                elif num_rooms == 1:
                    npc.x = new2_x
                    npc.y = new2_y

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

                # num_rooms wird 1 zugefügt, weil wir jetzt zum nächsten Raum kommen und der gerade eben erstellte Raum wird der Liste hinzugefügt
                rooms.append(new_room)
                num_rooms += 1

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

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False