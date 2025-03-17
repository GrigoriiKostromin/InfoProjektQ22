import tcod as libtcod

class BasicMonster:
    # AI zum bewegen. macht noch nichts, wird aber später eine Funktion, wie Pathfinding haben
    def take_turn(self, target, fov_map, game_map, entities,turn_num_monster):
        
        #Liste für Ergebnisse 
        results = []
        
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y): # Wenn diese Stelle in Sicht ist.
            
            
            
            if monster.distance_to(target) >= 2 and monster.name !="Riese": # Näher herantreten, wenn zu weit weg ist.
                monster.move_astar(target, entities, game_map)#movestar Algorhitmus
                

            #Riese bewegt sich anders
            elif monster.distance_to(target) >= 2 and turn_num_monster % 2  and monster.name =="Riese" :
                monster.move_astar(target, entities, game_map)


            #Liste wird erweitert, wenn Schaden genommen wird
            elif target.fighter.hp > 0 and monster.distance_to(target) <= 2: 
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
            print(turn_num_monster, "turn_num_monster")
           
        return results