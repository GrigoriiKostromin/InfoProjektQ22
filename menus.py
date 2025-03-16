import tcod as libtcod


def menu(con, header, options, width, screen_width, screen_height): # Hier die Parameter, die man zum erstellen des screens braucht
    if len(options) > 26: raise ValueError('Du kannst nicht mehr als 26 Gegenstaende haben') # Dass man nicht mehr Items als 26 haben kann

    # Hier wird die höhe der Kopfzeile ermittelt
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header) 
    height = len(options) + header_height

    # Hier wird ein Fenster erstellt, die das Menü darstellt
    window = libtcod.console_new(width, height)

    # Hier wird die Kopfzeile ausgegeben
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Hier werden die Optionen ausgegeben
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # Hier wird es an den Hauptbildschirm angehangen
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    # Hier wird ein Menü angezeigt, was die Items als Optionen auflistet
    if len(inventory.items) == 0:
        options = ['Inventar ist leer.']
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, background_image, screen_width, screen_height): # Wenn man daqs spiel startet, soll sich das öffnen
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER, # Schriftzug 1
                             'Katakomben')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER, # Schriftzug 2
                             'Von Greech und David')

    menu(con, '', ['Neues Spiel', 'Spiele weiter', 'Verlassen'], 24, screen_width, screen_height)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)