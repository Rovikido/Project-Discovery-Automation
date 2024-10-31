import numpy as np
import cv2

from app.utility.utility import dilate_poly_random


def get_polygon_from_matrix(matrix, epsilon=8, reduce_by=25, random_range=20):
    """
    Extracts polygon edge points from a matrix.

    Args:
        matrix (numpy.ndarray): Input matrix representing polygon edges.
        epsilon (int): Approximation accuracy parameter for contour detection.
        reduce_by (int): Amount by which to reduce the vertices' distances from the edges.
        random_range (int): Range for random distance variation.

    Returns:
        list: List of polygon edge point lists.
    """
    edge_points_list = []

    for num in np.unique(matrix):
        mask = np.uint8(matrix == num) * 255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, epsilon, True)
            vertices = [tuple(point[0]) for point in approx]
            vertices = dilate_poly_random(vertices, distance=-reduce_by, random_distance=True, random_range=random_range)
            edge_points_list.append(vertices)

    return edge_points_list


def get_distance_to_edge(edge_point_a, edge_point_b, point):
    """
    Calculates the squared distance between a point and a line segment.

    Args:
        edge_point_a (tuple): First endpoint of the line segment.
        edge_point_b (tuple): Second endpoint of the line segment.
        point (tuple): The point for which distance is calculated.

    Returns:
        float: Squared distance between the point and the line segment.
    """
    x1, y1 = edge_point_a
    x2, y2 = edge_point_b
    x3, y3 = point

    px = x2 - x1
    py = y2 - y1
    norm = px * px + py * py

    u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = dx * dx + dy * dy

    return dist


def get_distance_to_nearest_edge(point, polygon):
    """
    Calculates the distance from a point to the nearest edge of a polygon.

    Args:
        point (tuple): Coordinates of the point as (x, y).
        polygon (list): List of polygon edge points.

    Returns:
        float: Distance from the point to the nearest edge.
    """
    distances = [get_distance_to_edge(polygon[0], polygon[-1], point)]
    distances += [get_distance_to_edge(polygon[i], polygon[i + 1], point) for i in range(len(polygon) - 1)]
    return min(distances)


def expand_polygons(polygon_list, shape=(400, 420)):
    """
    Expands polygons to fill a specified shape.

    Args:
        polygon_list (list): List of polygons represented as lists of edge points.
        shape (tuple): Shape of the matrix to fill.

    Returns:
        list: Expanded polygon edge point lists.
    """
    matrix = np.zeros(shape, dtype=np.uint8)

    for y in range(shape[1]):
        for x in range(shape[0]):
            distances = [get_distance_to_nearest_edge((y, x), polygon) for polygon in polygon_list]
            matrix[x][y] = np.argmin(distances) + 1

    return get_polygon_from_matrix(matrix)
