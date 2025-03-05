import tcod as libtcod

class BasicMonster:
    # AI zum bewegen. macht noch nichts, wird aber später eine Funktion, wie Pathfinding haben
    def take_turn(self, target, fov_map, game_map, entities):
        #Liste für Ergebnisse 
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y): # Wenn diese Stelle in Sicht ist. 

            if monster.distance_to(target) >= 2: # Näher herantreten, wenn zu weit weg ist.
                monster.move_astar(target, entities, game_map)  #movestar Algorhitmus

            #Liste wird erweitert, wenn Schaden genommen wird
            elif target.fighter.hp > 0: 
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results