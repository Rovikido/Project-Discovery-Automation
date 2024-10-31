import time
import cv2

from app.screenshoting import get_screenshot_at
from app.polygon_detection import get_polygons_from_image, gen_rand_polygons_interface
from app.mouse_movement import execute_polygons, click_next
from app.utility.utility import shift_polygons
from app.utility.config_loader import SCREENSHOT_COORDS, CLICK_COORDS_TEMPLATE, MAX_ITERATIONS


SLEEP_TIME = 5


def main():
    # Used to give time for user to tab into app
    time.sleep(SLEEP_TIME)

    # Initial settings
    i = 30
    last_failed = False

    while i < MAX_ITERATIONS:
        try:
            # image = get_screenshot_at(*SCREENSHOT_COORDS)
            image = cv2.imread('app/test_images/output_image4.jpg')
            polygons = process_image(image, last_failed)
            shifted_polygons = shift_polygons(polygons, SCREENSHOT_COORDS[0], SCREENSHOT_COORDS[1])
            execute_polygons(shifted_polygons, *SCREENSHOT_COORDS)
            click_next(**CLICK_COORDS_TEMPLATE)
            print(f'Iteration {i} is finished')
            last_failed = False
            i += 1
        except Exception as e:
            handle_error(e, i)
            last_failed = True


def process_image(image, last_failed):
    if not last_failed:
        return get_polygons_from_image(image, debug=False)
    else:
        return gen_rand_polygons_interface(image)


def handle_error(exception, iteration):
    print(f'Error occurred in Iteration {iteration}!')
    print(exception)


if __name__ == "__main__":
    main()
