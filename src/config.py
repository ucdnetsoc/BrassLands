from utilities import get_path

Config = {
    'game': {
        'height': 640,
        'width': 800,
        'tile_width': 32,
        'wall_char': "W",
        'ground_char': '.'
    },
    'resources': {
        "ui": {
            'inventory': get_path("src/res/Inventory.png"),
            'icons': {
                'default': get_path("src/res/questionmark.png")
            }
        },
        'sprites': {
            'player': get_path("src/res/char.png"),
            'ground': get_path("src/res/ground.png"),
            'wall': get_path("src/res/rock.png")
        },
        'levels': {
            'level1': ""
        }
    }
}
