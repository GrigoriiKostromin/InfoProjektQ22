import tcod as libtcod

class BasicMonster:
    # AI zum bewegen. macht noch nichts, wird aber später eine Funktion, wie Pathfinding haben
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y): # Wenn diese Stelle in Sicht ist. 

            if monster.distance_to(target) >= 2: # Näher herantreten, wenn zu weit weg ist.
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0: 
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))