import numpy as np
import cv2
from utility import dilate_poly_random

def get_polygon_from_matrix(matrix, epsilon=8, reduce_by=20):
    edge_points_list = []
    for num in np.unique(matrix):
        mask = np.uint8(matrix == num) * 255
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            vertices = [tuple(point[0]) for point in approx]
            
            vertices = dilate_poly_random(vertices, distance=-reduce_by, random_distance=True, random_range=15)

            edge_points_list.append(vertices)
    
    return edge_points_list


def get_distance_to_edge(edge_point_a, edge_point_b, point):
    x1, y1 = edge_point_a
    x2, y2 = edge_point_b
    x3, y3 = point

    px = x2-x1
    py = y2-y1

    norm = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist = (dx*dx + dy*dy)

    return dist


def get_distance_to_nearest_edge(point, polygon):
    """
    Calculate the distance from a point to the nearest edge of a polygon.
    
    Parameters:
        point (tuple): Coordinates of the point as (x, y).
        polygon (shapely Polygon): The polygon object representing the geometrical object.
        
    Returns:
        float: Distance from the point to the nearest edge.
    """
    distances = [get_distance_to_edge(polygon[0], polygon[-1], point)]
    distances += [get_distance_to_edge(polygon[i], polygon[i+1], point) for i in range(len(polygon)-1)]
    return min(distances)


def expand_polygons(polygon_list, shape=(400, 420)):
    matrix = np.zeros(shape, dtype=np.uint8)
    for y in range(shape[1]):
        for x in range(shape[0]):
            distances = [get_distance_to_nearest_edge((y, x), polygon) for polygon in polygon_list]
            matrix[x][y] = np.argmin(distances)+1
    return get_polygon_from_matrix(matrix)
