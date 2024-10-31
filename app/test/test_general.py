import time
import cv2
import pytest

from app.screenshoting import get_screenshot_at
from app.polygon_detection import get_polygons_from_image, gen_rand_polygons_interface
from app.utility.utility import shift_polygons

from app.utility.config_loader import SCREENSHOT_COORDS


@pytest.fixture
def image():
    return cv2.imread('app/test_images/output_image4.jpg')


def test_get_polygons_from_image(image):
    polygons = get_polygons_from_image(image, debug=False)
    assert len(polygons)>0


def test_get_rand_polygons(image):
    polygons = gen_rand_polygons_interface(image)
    assert len(polygons)>0


def test_no_errors_shift_polygons(image):
    polygons = get_polygons_from_image(image, debug=False)
    shifted_polygons = shift_polygons(polygons, SCREENSHOT_COORDS[0], SCREENSHOT_COORDS[1])