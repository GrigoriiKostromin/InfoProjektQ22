class Entity:
    #Ein allgemeines Objekt zur Darstellung von Spielern, Feinden, Gegenständen usw.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        #Bewege Objekt um eine bestimmte Menge
        self.x += dx
        self.y += dy