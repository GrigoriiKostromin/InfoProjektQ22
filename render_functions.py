import tcod as libtcod

#Render Funktion für die Map
def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    #Karte nur aktualisieren, wenn sich das Sichtfeld ändert. Es wird nur das angezeigt, was im Sichtfeld war oder im Sichtfeld gewesen ist
    if fov_recompute:
        #Durchläuft jede Koordinate der Karte
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)  #Tile befindet sich im Sichtfeld
                wall = game_map.tiles[x][y].block_sight         #Wand definition im Sichtfeld

                #Wenn Tile im Sichtfeld ist werden helle Farben verwendet
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    #Bereits besuchte Tiles
                    game_map.tiles[x][y].explored = True

                #Wenn Tile besucht wurde, werden dunkle Farben verwendet
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    #Rendert alle Entititäten aus der Liste
    for entity in entities:
        draw_entity(con, entity, fov_map)
    
    """for entity in entities:
        draw_entity(con, entity, fov_map)"""

    #Kopiert Inhalt vom Root, um Rahmen anzuzeigen
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# Alles, was gerendert wurde, wird gelöscht, um ein neues Bild zu rendern. Es wird immer bei einer Aktion vom Spieler ein neues Frame erzeugt 
def clear_all(con, entities):
    for entity in entities:
        #console und Entititäten werden aus dem alten Bild entfernt und in ein Neues Hinzugefügt
        clear_entity(con, entity)

#Aussehen von Entititäten
def draw_entity(con, entity, fov_map):
    #Entititäten werden nur gerendert, wenn sie im Teil der Karte des Sichtfeldes sind
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def draw_entity1(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


#Reset nach Zeichnen (Bewegung)
def clear_entity(con, entity):
    #Das "Zeichen", das dieses Objekt darstellt, zu löschen. Also mit einem Leerzeichen zu ersetzten
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)