import tcod as libtcod

#Inizialisiert ein Sichtfeld basierend auf dem Maplayout aus game_map
def initialize_fov(game_map):
    #Parameter aus game_map werden weitergereicht
    fov_map = libtcod.map_new(game_map.width, game_map.height)

    #Durchläuft jede Koordinate der Karte
    for y in range(game_map.height):
        for x in range(game_map.width):
            #
            libtcod.map_set_properties(fov_map, x, y, 
                                       not game_map.tiles[x][y].block_sight,    #Tile ist transparent, wenn die Sicht nicht blockiert wird ("not", weil „block_sight=True“ nicht transparent bedeutet.)
                                       not game_map.tiles[x][y].blocked)        #Tile ist begehbar, wenn es nicht blockiert ist ("not", weil „blocked=True“ bedeutet nicht begehbar.)

    #Gibt eine "Sichtfeldkarte" aus
    return fov_map

#Die Methode updated das Sichtfeld 
def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    #Berechnen der Position mit der in tcod eingebauten Funktion.
    libtcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)