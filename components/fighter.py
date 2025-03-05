import tcod as libtcod

from game_messages import Message

class Fighter:
    #Klasse, mit dem man Entities das Kämpfen ermöglicht. Diese Klasse sorgt für eine Erweiterung der Entity Klasse. Ist aber nicht in die Entity Klasse implementiert, da es auch Objekte benötigt werden, welche keine "Kampfeigenschaften" besitzen sollten
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        
    #Funktion, um Schaden zu nehmen
    def take_damage(self, amount):
        #Liste für Ergebnisse
        results = []

        self.hp -= amount

        #Wenn Spieler tot, Liste erweitern    
        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):

        #Liste für Ergebnisse
        results = []

        damage = self.power - target.fighter.defense

        #Liste wird erweitert
        if damage > 0:
            target.fighter.take_damage(damage)
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})

            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})


        return results