import tcod as libtcod

from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp: # Wenn man volle Leben hat, dann kann man sich offensichtlich nicht heilen
        results.append({'consumed': False, 'message': Message('Du kannst dich nicht weiter heilen.', libtcod.yellow)})
    else:
        entity.fighter.heal(amount) # Hier wird die Heilungsmethode gecalled
        results.append({'consumed': True, 'message': Message('Deine Wunden wurden geheilt.', libtcod.green)})

    return results