import tcod as libtcod

#Render Funktion
def render_all(con, entities, game_map, screen_width, screen_height, colors):
    #Rebdert alle Kacheln auf der Karte
    for y in range(game_map.height):
        for x in range(game_map.width):
            #Sichtfeld
            wall = game_map.tiles[x][y].block_sight

            #Visuelle Unterscheidung zwischen Wand und nicht Wand
            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    #Rendert alle Entititäten aus der Liste
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

# Alle löschen 
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

#Aussehen von Entititäten
def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


#Reset nach Zeichnen (Bewegung)
def clear_entity(con, entity):
    #Das "Zeichen", das dieses Objekt darstellt, zu löschen
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)