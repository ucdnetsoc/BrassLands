import os
from utilities import RootGameDirectory

Config = {
    'game': {
        'height': 640,
        'width': 800,
        'tile_width': 32
    },
    'resources': {
        'sprites': {
            'player': os.path.join(RootGameDirectory(),"src/res/char.png")
        }
    }
}
