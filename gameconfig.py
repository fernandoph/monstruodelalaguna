level_map = [
'                         ',
'                         ',
'                         ',
'                         ',
'                         ',
'                  XXX    ',
'          XXXXXX         ',
'       P              X  ',
'       X                 ',
'     XXX    XX           ',
'XXXXXXXXX XXXXXXXXXXXXXXX'                         
]

# Game config
tile_size = 64
screen_width = 1600
screen_height = len(level_map) * tile_size

screen_size = (screen_width, screen_height)
screen_center = (screen_width // 2, screen_height // 2)
screen_caption = "El Monstruo de la Laguna"
screen_color = (0, 0, 0)
fps = 60
