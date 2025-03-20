import tcod as libtcod
from render_functions import RenderOrder
from game_states import GameStates
from game_messages import Message

#Wenn Spieler Tod ist
def kill_player(player):
    #Zeichen des Spielers wird zu einem rotem Prozentzeichen. Soll Blut darstellen
    player.char = '%'
    player.color = libtcod.dark_red
    is_dead = True

    #Todesnachricht
    return Message('Du bist gestorben! ESC ---> Hauptmenue', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    #Todesnachricht eines Monsters
    death_message = Message('{0} wurde eliminiert!'.format(monster.name.capitalize()), libtcod.orange)
    
    #Wenn Monster stirbt, wird es durch ein Blutfleck ersetzt und es werden Attribute des Monsters entfernt, sodass es nicht mehr fähig ist anzugreifen etc.
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Ueberreste des ' + monster.name +"s"
    monster.render_order = RenderOrder.CORPSE #Renderreihenfolge wird geeändert, sobald ein Monter stirbt. Wenn nicht, dann ist das Monster über dem Spieler

    return death_message