class Fighter:
    #Klasse, mit dem man Entities das Kämpfen ermöglicht. Diese Klasse sorgt für eine Erweiterung der Entity Klasse. Ist aber nicht in die Entity Klasse implementiert, da es auch Objekte benötigt werden, welche keine "Kampfeigenschaften" besitzen sollten
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power