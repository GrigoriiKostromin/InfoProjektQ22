import tcod as libtcod

import textwrap

#Nachrichtentext und Farbe
class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color

#Parameter für, umn eine Textbox zu erstellen
class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height


    def add_message(self, message):
        # NAchricht aufteilen, wenn nötig
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            # Wenn Puffer voll ist, wird die erste Zeile entfernt, um Platz für die neue Zeile zu schaffen
            if len(self.messages) == self.height:
                del self.messages[0]

            # Fügen die neue Zeile als mit dem Text und einer Farbe hinzu
            self.messages.append(Message(line, message.color))