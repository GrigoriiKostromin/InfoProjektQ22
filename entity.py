class Entity:
    #Ein allgemeines Objekt zur Darstellung von Spielern, Feinden, Gegenständen usw.
    def __init__(self, x, y, char, color, name, blocks=False): # Das "= False" zeigt quasi an, dass ein Wert nicht unbedingt übergeben werden muss. Wenn nichts übergeben wird, wird es automatisch erstmal auf false gesetzt 
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        #Bewege Objekt um eine bestimmte Menge
        self.x += dx
        self.y += dy


def get_blocking_entities_at_location(entities, destination_x, destination_y): # Wir übergeben quasi den Ort wo der Charakter sich hingeben möchte und welches Vieh das ist
    for entity in entities:  #Hier wird die ganze Entities Liste durchgegangen, um sich sicher zu sein, dass man nicht irgendwo reinläuft
        if entity.blocks and entity.x == destination_x and entity.y == destination_y: # Hier wird es verglichen, um wen es sich handelt
            return entity # Die Entity wird ausgegegeben um wen es sich handelt, und so kann man dann quasi machen, dass wenn der Spieler in einen Buff reinläuft er was anderes bekommt, wie als wenn er in einen Gegner reinrennt

    return None # Falls er nirgends reinrennt passiert nix