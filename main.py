from time import sleep
from cv2 import imread

from app.screenshoting import get_screenshot_at
from app.polygon_detection import get_polygons_from_image
from app.mouse_movement import execute_polygons, click_next

from app.utility import shift_polygons


if __name__ == "__main__":
    x=1084
    y=311
    w=448
    h=416

    sleep(5)
    i = 0
    while i < 195:
        try:
            image = get_screenshot_at(x, y, w, h)
            # image = imread('output_image4.jpg') 
            polygons = get_polygons_from_image(image, debug=False)
            polygons = shift_polygons(polygons, x, y)
            execute_polygons(polygons, x, y, w, h)
            click_next(x=1868, y=742, iw=300, ih=16)
            print(f'Itteration {i} is finished')
            i+=1
        except Exception as e:
            print(f'Error occured in Itteration {i}!')
            print(e)
            
    # print(polygons.shape)
    # get_clusters(data_from_image)