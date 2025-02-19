import math
class Entity:
    #Ein allgemeines Objekt zur Darstellung von Spielern, Feinden, Gegenständen usw.
    # Das "= False" zeigt quasi an, dass ein Wert nicht unbedingt übergeben werden muss. Wenn nichts übergeben wird, wird es automatisch erstmal auf false gesetzt 
    # fighter und ai Komponenten sind optional, da Objekte auch Gegenstände darstellen können
    def __init__(self, x, y, char, color, name, blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

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

    def distance_to(self, other): #Distabz zu anderen Enteties wird berechnet. Zb Spieler
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2) # Pythagoras, um die Länge des direkten Weges zu berechnen

def get_blocking_entities_at_location(entities, destination_x, destination_y): # Wir übergeben quasi den Ort wo der Charakter sich hingeben möchte und welches Vieh das ist
    for entity in entities:  #Hier wird die ganze Entities Liste durchgegangen, um sich sicher zu sein, dass man nicht irgendwo reinläuft
        if entity.blocks and entity.x == destination_x and entity.y == destination_y: # Hier wird es verglichen, um wen es sich handelt
            return entity # Die Entity wird ausgegegeben um wen es sich handelt, und so kann man dann quasi machen, dass wenn der Spieler in einen Buff reinläuft er was anderes bekommt, wie als wenn er in einen Gegner reinrennt

    return None # Falls er nirgends reinrennt passiert nix