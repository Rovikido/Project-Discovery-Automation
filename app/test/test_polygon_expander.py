import numpy as np
import pytest
from app.polygon_expander import get_polygon_from_matrix


@pytest.fixture
def matrix():
    return np.array([[0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 1, 0, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0]])

def test_get_polygon_from_matrix_type(matrix):
    polygons = get_polygon_from_matrix(matrix)
    assert isinstance(polygons, list)


def test_get_polygon_from_matrix_length(matrix):
    polygons = get_polygon_from_matrix(matrix)
    assert len(polygons) == 2


def test_get_polygon_from_matrix_vertices(matrix):
    polygons = get_polygon_from_matrix(matrix)
    assert len(polygons[0]) == 1


def test_get_polygon_from_matrix_values(matrix):
    polygons = get_polygon_from_matrix(matrix)
    for polygon in polygons:
        for vertex in polygon:
            assert len(vertex) == 2


def test_get_polygon_from_matrix_empty():
    polygons = get_polygon_from_matrix(np.zeros((5, 5)))
    assert len(polygons) == 1