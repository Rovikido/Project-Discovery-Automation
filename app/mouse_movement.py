import pyautogui
import bezeMouse.mouse as bzm
from time import sleep

from app.utility.utility import random_normal, random_unexpected_normal


def execute_polygons(polygon_list, x, y, width, height):
    """
    Execute a series of mouse movements and clicks based on a list of polygons.

    Args:
        polygon_list (list): List of polygons where each polygon is a list of points (x, y).
        x (int): X-coordinate of the top-left corner of the area to move the mouse to.
        y (int): Y-coordinate of the top-left corner of the area to move the mouse to.
        width (int): Width of the area to move the mouse to.
        height (int): Height of the area to move the mouse to.
    """
    deviation = round(random_unexpected_normal(10, 20, additional_range=(2, 3), additional_chance=0.005))
    speed = round(random_unexpected_normal(1, 3, additional_range=(2, 7)))
    
    bzm.move_to_area(x, y, width, height, deviation=deviation, speed=speed, delete_every_n=8)
    
    for polygon in polygon_list:
        process_polygon(polygon)


def process_polygon(polygon):
    """
    Process a single polygon by iterating through its points and performing mouse movements and clicks.

    Args:
        polygon (list): A polygon represented as a list of points (x, y).
    """
    polygon_with_first_point = polygon + [polygon[0],]
    print(polygon_with_first_point)
    
    for point in polygon_with_first_point:
        move_and_click(point)


def move_and_click(point):
    """
    Move the mouse to a specified point and perform a click.

    Args:
        point (tuple): A point (x, y) to move the mouse to and click.
    """
    initial_pos = pyautogui.position()
    deviation = round(random_unexpected_normal(10, 20, additional_range=(2, 3), additional_chance=0.005))
    speed = round(random_unexpected_normal(1, 2, additional_range=(2, 7), shift_mu=-0.3))
    
    bzm.move(bzm.mouse_bez(init_pos=initial_pos, fin_pos=point, deviation=deviation, speed=speed, delete_every_n=4))
    bzm.real_click()
    sleep(random_unexpected_normal(0.01, 0.2, additional_range=(1, 7), additional_chance=0.002))


def click_next(x=1866, y=740, width=304, height=24):
    """
    Move the mouse to the specified area and perform a sequence of clicks.

    Args:
        x (int): X-coordinate of the top-left corner of the area to move the mouse to.
        y (int): Y-coordinate of the top-left corner of the area to move the mouse to.
        width (int): Width of the area to move the mouse to.
        height (int): Height of the area to move the mouse to.
    """
    sleep_before_click()
    move_to_click_area(x, y, width, height)
    perform_click_sequence()


def sleep_before_click():
    """
    Sleep for a randomized duration before performing a click.
    """
    sleep(random_unexpected_normal(0.4, 3, additional_range=(6, 100), additional_chance=0.004, shift_mu=-0.5))


def move_to_click_area(x, y, width, height):
    """
    Move the mouse to the specified area.

    Args:
        x (int): X-coordinate of the top-left corner of the area to move the mouse to.
        y (int): Y-coordinate of the top-left corner of the area to move the mouse to.
        width (int): Width of the area to move the mouse to.
        height (int): Height of the area to move the mouse to.
    """
    deviation = round(random_unexpected_normal(10, 20, additional_range=(2, 3), additional_chance=0.005))
    speed = round(random_unexpected_normal(1, 3, additional_range=(2, 7)))
    bzm.move_to_area(x, y, width, height, deviation=deviation, speed=speed, delete_every_n=6)


def perform_click_sequence():
    """
    Perform a sequence of clicks with randomized intervals.
    """
    click_with_sleep()
    click_with_sleep()
    click_with_sleep()
    sleep(random_unexpected_normal(1.7, 2.3))
    bzm.real_click()
    sleep(random_unexpected_normal(0.1, 0.3))


def click_with_sleep():
    """
    Perform a click and sleep for a randomized short duration.
    """
    bzm.real_click()
    sleep(random_unexpected_normal(0.2, 0.3))
