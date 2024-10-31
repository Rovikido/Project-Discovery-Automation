import json

CONFIG_PATH = 'config.json'

def load_config():
    with open(CONFIG_PATH, 'r') as config_file:
        return json.load(config_file)


config = load_config()

SCREENSHOT_COORDS = (
    config['SCREENSHOT_COORDS']['x'],
    config['SCREENSHOT_COORDS']['y'],
    config['SCREENSHOT_COORDS']['w'],
    config['SCREENSHOT_COORDS']['h']
)

CLICK_COORDS_TEMPLATE = {
    'x': SCREENSHOT_COORDS[0] + config['CLICK_OFFSET']['x_offset'],
    'y': SCREENSHOT_COORDS[1] + config['CLICK_OFFSET']['y_offset'],
    'width': config['CLICK_COORDS']['width'],
    'height': config['CLICK_COORDS']['height']
}

MAX_ITERATIONS = config.get('MAX_ITERATIONS', 200)
