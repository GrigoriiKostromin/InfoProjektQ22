#in der Klasse wird der Effekt und die Anzahl der Ausrüstbaren Items dargestellt
class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
        #Anzahl an Ausrüstmöglichkeiten
        self.slot = slot
        #Boni durch die Ausrüstung
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus