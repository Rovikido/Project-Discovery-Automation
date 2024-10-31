import pytest
import numpy as np
from app.utility.utility import polygon_contains_polygon, random_normal, random_unexpected_normal, dilate_poly, dilate_poly_random, get_centroid_of_polygon, shift_polygons


def test_polygon_contains_polygon():
    polygon1 = [(0, 0), (0, 2), (2, 2), (2, 0)]
    polygon2 = [(1, 1), (1, 1.5), (1.5, 1.5), (1.5, 1)]
    assert polygon_contains_polygon(polygon1, polygon2) == True


def test_random_normal():
    start = 0
    end = 10
    num = random_normal(start, end)
    assert start <= num <= end


def test_random_unexpected_normal():
    start = 0
    end = 10
    num = random_unexpected_normal(start, end, additional_range=(20, 30), additional_chance=0.5)
    assert (start <= num <= end) or (20 <= num <= 30)


def test_dilate_poly():
    poly = np.array([(0, 0), (0, 2), (2, 2), (2, 0)])
    distance = 1
    dilated_poly = dilate_poly(poly, distance)
    assert isinstance(dilated_poly, np.ndarray)
    assert dilated_poly.shape == poly.shape


def test_dilate_poly_random():
    poly = np.array([(0, 0), (0, 2), (2, 2), (2, 0)])
    distance = 1
    dilated_poly = dilate_poly_random(poly, distance)
    assert isinstance(dilated_poly, np.ndarray)
    assert dilated_poly.shape == poly.shape


def test_get_centroid_of_polygon():
    vertices = [(0, 0), (0, 2), (2, 2), (2, 0)]
    centroid = get_centroid_of_polygon(vertices)
    assert isinstance(centroid, tuple)
    assert len(centroid) == 2


def test_shift_polygons():
    polygons = [[(0, 0), (0, 2), (2, 2), (2, 0)]]
    x, y = 1, 1
    shifted_polygons = shift_polygons(polygons, x, y)
    assert isinstance(shifted_polygons, list)
    assert len(shifted_polygons) == len(polygons)
    assert all(isinstance(polygon, list) for polygon in shifted_polygons)