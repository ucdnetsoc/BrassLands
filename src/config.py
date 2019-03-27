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
            'menu': get_path("src/res/ui/menu.png"),
            'inventory': get_path("src/res/ui/Inventory.png"),
            'hover': get_path("src/res/ui/hover.png"),
            'fonts': {
                'tooltip': get_path("src/res/ui/fonts/tooltip.ttf")
            },
            'icons': {
                'default': get_path("src/res/ui/icons/questionmark.png")
            }
        },
        'sprites': {
            'player': get_path("src/res/sprites/char.png"),
            'ground': get_path("src/res/sprites/ground.png"),
            'wall': get_path("src/res/sprites/rock.png")
        },
        'levels': {
            'level1': get_path("src/res/levels/example.lvl")
        }
    }
}
