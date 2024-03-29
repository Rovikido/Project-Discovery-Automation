import pyautogui, sys   
import bezeMouse.mouse as bzm
from time import sleep

from app.utility import random_normal, random_unexpected_normal


def execute_polygons(polygon_list, x, y, iw, ih):
    bzm.move_to_area(x, y, iw, ih, 
                     deviation=round(random_unexpected_normal(10, 20, additional_range=(2, 3), additional_chance=0.005)), 
                     speed=round(random_unexpected_normal(1, 3, additional_range=(2, 7))), 
                     delete_every_n=8)
    for polygon in polygon_list:
        polygon += tuple([polygon[0]])
        print(polygon)
        for point in polygon:
            # print(point)
            initial_pos = tuple([pyautogui.position()[0], pyautogui.position()[1]])
            bzm.move(bzm.mouse_bez(init_pos=initial_pos, fin_pos=point,
                          deviation=round(random_unexpected_normal(10, 20, additional_range=(2, 3), additional_chance=0.005)),
                          speed=round(random_unexpected_normal(1, 2, additional_range=(2, 7), shift_mu=-0.3)), 
                          delete_every_n=4))
            bzm.real_click()
            sleep(random_unexpected_normal(0.01, 0.2, additional_range=(1, 7), additional_chance=0.002))
            #click

#1866 740  2170 764
            
def click_next(x=1866, y=740, iw=304, ih=24):
    sleep(random_unexpected_normal(0.4, 3, additional_range=(6, 100), additional_chance=0.004, shift_mu=-0.5))
    bzm.move_to_area(x, y, iw, ih, 
                     deviation=round(random_unexpected_normal(10, 20, additional_range=(2, 3), additional_chance=0.005)), 
                     speed=round(random_unexpected_normal(1, 3, additional_range=(2, 7))), 
                     delete_every_n=6)
    sleep(random_unexpected_normal(0.2, 0.3))
    bzm.real_click()
    sleep(random_unexpected_normal(0.2, 0.3))
    bzm.real_click()
    sleep(random_unexpected_normal(0.2, 0.3))
    bzm.real_click()
    sleep(random_unexpected_normal(1.7, 2.3))
    bzm.real_click()
    sleep(random_unexpected_normal(0.1, 0.3))

