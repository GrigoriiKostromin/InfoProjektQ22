from enum import Enum 

# enum kommt von "enumerationen", also Aufzählungen. Also das hilft um ganz lange Aufzählungen und sowas durchzuführen. 
#    also statt beispielsweise "1, 2, 3, usw." durchzuzählen kann man das hier ganz einfach machen. Das starten des Durchzählens wird in engine geregelt.

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2



# Hier wird immer geschaut, wer sich als nächstes bewegen darf. Entweder der Spieler, oder die Gegner