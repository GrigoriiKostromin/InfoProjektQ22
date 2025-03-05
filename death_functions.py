import tcod as libtcod

from game_states import GameStates

#Wenn Spieler Tod ist
def kill_player(player):
    #Zeichen des Spielers wird zu einem rotem Prozentzeichen. Soll Blut darstellen
    player.char = '%'
    player.color = libtcod.dark_red

    #Todesnachricht
    return 'You died!', GameStates.PLAYER_DEAD


def kill_monster(monster):
    #Todesnachricht eines Monsters
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    #Wenn Monster stirbt, wird es durch ein Blutfleck ersetzt und es werden Attribute des Monsters entfernt, sodass es nicht mehr fähig ist anzugreifen etc.
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name

    return death_message