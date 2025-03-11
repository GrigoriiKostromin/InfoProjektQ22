from enum import Enum 

# enum kommt von "enumerationen", also Aufz�hlungen. Also das hilft um ganz lange Aufz�hlungen und sowas durchzuf�hren. 
#    also statt beispielsweise "1, 2, 3, usw." durchzuz�hlen kann man das hier ganz einfach machen. Das starten des Durchz�hlens wird in engine geregelt.

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
    DROP_INVENTORY = 5



# Hier wird immer geschaut, wer sich als n�chstes bewegen darf. Entweder der Spieler, oder die Gegner