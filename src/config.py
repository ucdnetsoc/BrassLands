import os
from utilities import RootGameDirectory

path = lambda string : os.path.join(RootGameDirectory(),string);

Config = {
    'game': {
        'height': 640,
        'width': 800,
        'tile_width': 32
    },
    'resources': {
        'sprites': {
            'player': path("src/res/char.png")
        }
    }
}

