from equipment_slots import EquipmentSlots

#Klasse, in der die Ausrüstung erstellt wird
class Equipment:
    def __init__(self, main_hand=None, off_hand=None, armor=None, special_slot=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.armor = armor
        self.special_slot = special_slot

    #Hier werden die Boni, für die jeweiligen equipmentoptinen definiert (HP)
    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus
        
        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.max_hp_bonus
        
        if self.special_slot and self.off_hand.equippable:
            bonus += self.special_slot.equippable.max_hp_bonus


        return bonus

    #Hier werden die Boni, für die jeweiligen equipmentoptinen definiert (POWER)
    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus
        
        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.power_bonus
        
        if self.special_slot and self.off_hand.equippable:
            bonus += self.special_slot.equippable.power_bonus

        return bonus

    #Hier werden die Boni, für die jeweiligen equipmentoptinen definiert (DEFENSE)
    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.defense_bonus
        
        if self.special_slot and self.off_hand.equippable:
            bonus += self.special_slot.equippable.defense_bonus

        return bonus

    #In dieser funktion wird as Ausrüsten der Items dargestellt
    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        #Die Haupthand als Beispiel
        if slot == EquipmentSlots.MAIN_HAND:
            #Wenn wir ein Item bereits ausgerüstet haben und ein neues Ausrüsten wollen, wird das vorherige entfernt.
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                #Wenn das Item bereits ausgerüstet ist, und man es nochmal ausrüsten möchte, wird es entfernt.
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        #Hier genau der selbe Prozess
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.ARMOR:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        
        elif slot == EquipmentSlots.SPECIAL_SLOT:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
