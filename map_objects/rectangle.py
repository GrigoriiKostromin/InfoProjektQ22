
#Erstellen einer Klasse für einfache Raumkreation (von x1, bis x2... um später die Koordinaten zu haben)
class Rect:
    def __init__(self, x, y, w, h): # w für weite und h für höhe. x1 & y1 für die Koordinate oben links und die mit zwei für unten rechts
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # Wird positiv ausgegeben, wenn der Raum einen anderen schneidet.
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)