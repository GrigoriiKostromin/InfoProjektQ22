import tcod as libtcod

from game_messages import Message


class Inventory: # Hier werden sp�ter die Gegenst�nde im inventar gespeichert
    def __init__(self, capacity):
        self.capacity = capacity # Maximale Anzahl an Gegenst�nden
        self.items = [] # Hier wird die Liste dann gef�llt

    def add_item(self, item): # Ein Item zum Inventar hinzuf�gen
        results = [] # Sodass mehrere Items gleichzeitig hinzugef�gt werden k�nnen

        if len(self.items) >= self.capacity: # Wenn man zu viele Sachen schon tr�gt
            results.append({
                'item_added': None, # Es wird nix hinzugef�gt
                'message': Message('Es kann nichts aufgehoben werden. Das Inventar ist voll.', libtcod.yellow)
            })
        else:
            results.append({ # Hier wird dann ein Item zu der Liste hinzugef�gt (bzw. gleich)
                'item_added': item,
                'message': Message('Es wurde {0} aufgehoben!'.format(item.name), libtcod.blue)
            })

            self.items.append(item) # Hier passiert das dann

        return results 

    def use(self, item_entity, **kwargs): 
        results = [] # Liste an Dingen die passieren sollen

        item_component = item_entity.item

        if item_component.use_function is None: # Wenn Items keine Funktion haben, dann passiert nichts und es wird folgende Nachricht ausgegeben
            results.append({'message': Message('{0} kann nicht benutzt werden'.format(item_entity.name), libtcod.yellow)})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs) # Hier wird dann die Funktion vom Item gecalled, wenn man es konsumieren m�chte

            for item_use_result in item_use_results: 
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity) # Nach der Verwendung wird dann das Item aus dem Inventar entfernt

            results.extend(item_use_results)

        return results

    def remove_item(self, item): # Funktion um das Item aus dem Inventar zu entfernen
        self.items.remove(item)


    def drop_item(self, item):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('{0} wurde fallen gelassen'.format(item.name),
                                                                 libtcod.yellow)})

        return results