from time import sleep
from cv2 import imread

from app.screenshoting import get_screenshot_at
from app.polygon_detection import get_polygons_from_image, gen_rand_polygons_interface
from app.mouse_movement import execute_polygons, click_next

from app.utility import shift_polygons


if __name__ == "__main__":
    x=
    y=
    w=
    h=

    sleep(5)
    i = 0
    last_failed = False
    while i < 195:
        try:
            image = get_screenshot_at(x, y, w, h)
            # image = imread('app/output_image4.jpg')  
            if not last_failed:
                polygons = get_polygons_from_image(image, debug=False)
            else:
                polygons = gen_rand_polygons_interface(image)
            polygons = shift_polygons(polygons, x, y)
            execute_polygons(polygons, x, y, w, h)
            click_next(x=, y=, iw=300, ih=16) # continue button
            print(f'Itteration {i} is finished')
            last_failed = False
            i+=1
        except Exception as e:
            print(f'Error occured in Itteration {i}!')
            last_failed = True
            print(e)
            
    # print(polygons.shape)
    # get_clusters(data_from_image)