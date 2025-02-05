
#Erstellen einer Klasse für einfache Raumkreation (von x1, bis x2... um später die Koordinaten zu haben)
class Rect:
    def __init__(self, x, y, w, h): # w für weite und h für höhe. x1 & y1 für die Koordinate oben links und die mit zwei für unten rechts
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h