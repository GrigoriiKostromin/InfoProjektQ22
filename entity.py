import math
import tcod as libtcod
from render_functions import RenderOrder
from components.item import Item

class Entity:
    #Ein allgemeines Objekt zur Darstellung von Spielern, Feinden, Gegenständen usw.
    # Das "= False" zeigt quasi an, dass ein Wert nicht unbedingt übergeben werden muss. Wenn nichts übergeben wird, wird es automatisch erstmal auf false gesetzt 
    # fighter und ai Komponenten sind optional, da Objekte auch Gegenstände darstellen können
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None, stairs=None, equipment=None, equippable=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.equipment = equipment
        self.equippable = equippable

        #Untescheidung zwishen unterschiedlichen Entititäten. Nicht, dass ein Gegner versehentlich die Werte von einem anderen annimmt. Das gillt für alle Entititäten.
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        #Bewege Objekt um eine bestimmte Menge
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities): #AI für die Bewegung eines Enteties
        dx = target_x - self.x  # Abstand vom Ziel zum Entity
        dy = target_y - self.y  # Abstand vom Ziel zum Entity
        distance = math.sqrt(dx ** 2 + dy ** 2)# Pythagoras, um die Länge des direkten Weges zu berechnen

        #Wenn die Koordinate durch die Länge geteilt wird, kommt eine Zahl raus, die zwischhen -1 und 1 liegt, mit außnahme der 0. Es nicht 0 sein. Da es dizemalzahl rauskommt und wir nur mit Int arbeiten, runden wir das jeweil auf -1 oder 1. Diese Rechnung ist nötig, um die Bewegungsrichtung zu ermitteln
        dx = int(round(dx / distance))  #-1 oder 1
        dy = int(round(dy / distance))  #-1 oder 1


        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                    get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)): # Wenn Tile nicht von der Map oder anderen Entititäten blockiert wird, kann sich die Entitität bewegen.
            self.move(dx, dy)

    
    def distance_to(self, other): #Distanz zu anderen Enteties wird berechnet. Zb Spieler
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2) # Pythagoras, um die Länge des direkten Weges zu berechnen
    

    def distance(self, x, y): #Distanz zu einem bestimmten Ziel
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
    


    def move_astar(self, target, entities, game_map):  #https://en.wikipedia.org/wiki/A*_search_algorithm
        # Erstellen Sie eine Sichtfeld-Karte, die die Abmessungen der Karte hat
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scanne die aktuelle Karte in jeder Runde und setze alle Wände als unbegehbar

        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scanne alle Objekte, um zu sehen, ob es Objekte gibt, um die herum navigiert werden muss.
        # Überprüfe auch, ob es sich bei dem Objekt nicht um dich selbst oder das Ziel handelt (damit der Start- und der Endpunkt frei sind).
        # Die KI-Klasse behandelt die Situation, wenn sich self neben dem Ziel befindet, so dass sie diese A*-Funktion ohnehin nicht verwenden wird.
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Legen Sie die Kachel als Wand fest, so dass sie umfahren werden muss
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Finde einen A* Weg
        # Die 1,41 ist die normale diagonale Kosten der Bewegung, es kann als 0,0 gesetzt werden, wenn diagonale Bewegungen verboten sind.
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Berechnung des Weges zwischen den eigenen Koordinaten und den Koordinaten des Ziels
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Prüfe, ob der Pfad existiert, und in diesem Fall auch, ob er kürzer als 25 Kacheln ist.
        # Die Pfadgröße ist wichtig, wenn man möchte, dass das Monster alternative, längere Pfade benutzt (z.B. durch andere Räume), wenn sich der Spieler z.B. in einem Korridor befindet.
        # Es ist sinnvoll, die Pfadgröße relativ niedrig zu halten, um die Monster davon abzuhalten, auf der Karte herumzulaufen, wenn es einen alternativen Pfad gibt, der sehr weit weg ist.
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Suche nach den nächsten Koordinaten im berechneten vollständigen Pfad
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Setzt die eigenen Koordinaten auf die nächste Pfadkachel
                self.x = x
                self.y = y
        else:
            # Behalte die alte Bewegungsfunktion als Backup, so dass, wenn es keine Pfade gibt (zum Beispiel ein anderes Monster einen Korridor blockiert)
            # es trotzdem versucht, sich auf den Spieler zu bewegen (näher an die Korridoröffnung)
            self.move_towards(target.x, target.y, game_map, entities)

            # Löschen Sie den Pfad, um Speicher freizugeben.
        libtcod.path_delete(my_path)



def get_blocking_entities_at_location(entities, destination_x, destination_y): # Wir übergeben quasi den Ort wo der Charakter sich hingeben möchte und welches Vieh das ist
    for entity in entities:  #Hier wird die ganze Entities Liste durchgegangen, um sich sicher zu sein, dass man nicht irgendwo reinläuft
        if entity.blocks and entity.x == destination_x and entity.y == destination_y: # Hier wird es verglichen, um wen es sich handelt
            return entity # Die Entity wird ausgegegeben um wen es sich handelt, und so kann man dann quasi machen, dass wenn der Spieler in einen Buff reinläuft er was anderes bekommt, wie als wenn er in einen Gegner reinrennt

    return None # Falls er nirgends reinrennt passiert nix

