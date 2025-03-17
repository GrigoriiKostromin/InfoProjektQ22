import tcod as libtcod

class BasicMonster:
    # AI zum bewegen. macht noch nichts, wird aber später eine Funktion, wie Pathfinding haben
    def take_turn(self, target, fov_map, game_map, entities,turn_num_monster):
        
        #Liste für Ergebnisse 
        results = []
        
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y): # Wenn diese Stelle in Sicht ist.
            
            
            
            if monster.distance_to(target) >= 2 and monster.name !="Riese" and monster.name !="Spinne": # Näher herantreten, wenn zu weit weg ist.
                monster.move_astar(target, entities, game_map)#movestar Algorhitmus
                

            #Riese bewegt sich jeden zweiten Zug
            elif monster.distance_to(target) >= 2 and turn_num_monster % 2  and monster.name =="Riese" :
                monster.move_astar(target, entities, game_map)

            elif monster.distance_to(target) >= 2 and monster.name =="Spinne" :
                monster.move_astar(target, entities, game_map)
                if monster.distance_to(target) > 1:
                    monster.move_astar(target, entities, game_map)
            

            elif target.fighter.hp > 0 and monster.distance_to(target) <= 2 and monster.name =="Riese" and turn_num_monster % 2: 
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
            

            #Liste wird erweitert, wenn Schaden genommen wird
            elif target.fighter.hp > 0 and monster.distance_to(target) <= 2 and monster.name !="Riese": 
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
            print(turn_num_monster, "turn_num_monster")
           
        return results