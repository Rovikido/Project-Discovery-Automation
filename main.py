from time import sleep
from cv2 import imread

from screenshoting import get_screenshot_at
from polygon_detection import get_polygons_from_image
from mouse_movement import execute_polygons, click_next

from utility import shift_polygons


if __name__ == "__main__":
    x=1084
    y=311
    w=448
    h=416
    sleep(5)
    for i in range(50):
        image = get_screenshot_at(x, y, w, h)
        # image = imread('output_image4.jpg') 
        polygons = get_polygons_from_image(image, debug=False)
        polygons = shift_polygons(polygons, x, y)
        execute_polygons(polygons, x, y, w, h)
        click_next(x=1866, y=740, iw=304, ih=24)
    # print(polygons.shape)
    # get_clusters(data_from_image)