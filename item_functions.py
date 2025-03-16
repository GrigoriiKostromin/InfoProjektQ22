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

#Funktion für Blitzzauber. Der Blitzzauber schlägt auf den nächten Gegegner im Sichtfeld des Spielers ein.
def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    #Die maximale Reichweite + 1 ist die nächste Distanz
    closest_distance = maximum_range + 1


    for entity in entities:
        #Wenn Entenität nicht der nutzer des Zauber ist und im Sichtfeld ist. Es wird die Distanz zwischen dem Nutzer und der Entität berechnet
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            #Wenn die Disntanz kleiner, als die nächte Distanz ist, wird die Distnaz zur nächten Distanz
            if distance < closest_distance:
                target = entity
                closest_distance = distance

    #Wenn das Ziel in der Reichweite des Zaubers ist, bekommt der Gegner schaden.
    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('Blitzzauber trifft {0}. Der Schaden betaegt: {1}'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))

    #Wenn das Ziel in der Reichweite des Zaubers ist, bekommt der Gegner kein schaden.
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('Kein Gegner ist in der Reichweite', libtcod.red)})

   #Das Erbenis wird ausgegeben 
    return results


#Funktion für Feuerballzuaber
def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    #Wenn das Ziel nicht in der Reichweite ist, schlägt der Angriff fehl.
    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('Kein Gegner ist in der Reichweite', libtcod.yellow)})
        return results
    #Log Nachricht, wenn der Zauber funktioniert
    results.append({'consumed': True, 'message': Message('Der Feuerball explodierte und zerstörte alles im Umkreis von {0} Kacheln!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('{0} erleidet {1} Schaden durch Verbrennung.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results