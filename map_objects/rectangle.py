
#Erstellen einer Klasse f�r einfache Raumkreation (von x1, bis x2... um sp�ter die Koordinaten zu haben)
class Rect:
    def __init__(self, x, y, w, h): # w f�r weite und h f�r h�he. x1 & y1 f�r die Koordinate oben links und die mit zwei f�r unten rechts
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h