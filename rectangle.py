
#Erstellen einer Klasse f�r einfache Raumkreation (von x1, bis x2... um sp�ter die Koordinaten zu haben)
class Rect:
    def __init__(self, x, y, w, h): # w f�r weite und h f�r h�he. x1 & y1 f�r die Koordinate oben links und die mit zwei f�r unten rechts
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self): #Mittelpunkt berechnung
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)