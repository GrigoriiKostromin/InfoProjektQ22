class Fighter:
    #Klasse, mit dem man Entities das Kämpfen ermöglicht. Diese Klasse sorgt für eine Erweiterung der Entity Klasse. Ist aber nicht in die Entity Klasse implementiert, da es auch Objekte benötigt werden, welche keine "Kampfeigenschaften" besitzen sollten
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        
    #Funktion, um Schaden zu nehmen
    def take_damage(self, amount):
        self.hp -= amount

    #Funktion, um Schaden zu machen
    def attack(self, target):
        damage = self.power - target.fighter.defense

        # Schaden in der Konsole ausgeben
        if damage > 0:
            target.fighter.take_damage(damage)
            print('{0} attacks {1} for {2} hit points.'.format(self.owner.name.capitalize(), target.name, str(damage)))
        else:
            print('{0} attacks {1} but does no damage.'.format(self.owner.name.capitalize(), target.name))