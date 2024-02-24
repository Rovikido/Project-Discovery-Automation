from random import random, randrange, uniform
import numpy as np


def random_normal(start, end=0, shift_mu=0, scale_sigma=1):
    """
    Generate a random number that follows a normal distribution within a specified range.

    Parameters:
        start (float): Start of the range.
        end (float): End of the range.
        shift_mu = 0 (float): Value, added to mean. Beware of abs(shift_mu) > (end-start)/2.
        scale_sigma = 1 (float): Multiplies standart deviation by value.

    Returns:
        float: Random number within the specified range and following the normal distribution.
    """
    if start>end:
        end, start = start, end
    
    mu = (end+start)/2 + shift_mu
    sigma = (end-start)/9 * scale_sigma
    for _ in range(1000):
        num = np.random.normal(mu, sigma)
        if start <= num <= end:
            return num
    return uniform(start, end)


def random_unexpected_normal(start, end=0, additional_range=None, additional_chance = 0.01, shift_mu=0, scale_sigma=1):
    if random() <= additional_chance and additional_range:
        return uniform(additional_range[0],additional_range[1])
    return random_normal(start, end, shift_mu=shift_mu, scale_sigma=scale_sigma)


def dilate_poly(poly, distance):
    centroid = np.mean(poly, axis=0)
    vectors = poly - centroid
    norms = np.linalg.norm(vectors, axis=1)
    normalized_vectors = vectors / norms[:, np.newaxis]
    expanded_points = centroid + (normalized_vectors * (norms + distance)[:, np.newaxis])
    return np.int32(expanded_points)


def dilate_poly_random(poly, distance, random_distance=False, random_range=2):
    centroid = np.mean(poly, axis=0)
    vectors = poly - centroid
    norms = np.linalg.norm(vectors, axis=1)
    if random_distance:
        random_distances = np.random.uniform(-random_range, random_range, size=len(norms))
        distances = distance + random_distances
    else:
        distances = np.full_like(norms, distance)
    normalized_vectors = vectors / norms[:, np.newaxis]
    expanded_points = centroid + (normalized_vectors * (norms + distances)[:, np.newaxis])
    return np.int32(expanded_points)


def get_centroid_of_polygon(vertices, round_=False):
    """
    Calculate the centroid of a polygon given its vertices.

    Parameters:
    vertices (list of tuples): List of (x, y) coordinates of the vertices.

    Returns:
    centroid (tuple): (x, y) coordinates of the centroid.
    """
    vertices = np.array(vertices)

    shifted_vertices = np.roll(vertices, 1, axis=0)

    cross_product = np.cross(vertices, shifted_vertices)

    area = 0.5 * np.sum(cross_product)

    centroid_x = np.sum((vertices[:, 0] + shifted_vertices[:, 0]) * cross_product) / (6 * area)
    centroid_y = np.sum((vertices[:, 1] + shifted_vertices[:, 1]) * cross_product) / (6 * area)
    if round_:
        centroid_x = round(centroid_x)
        centroid_y = round(centroid_y)
    return centroid_x, centroid_y


def shift_polygons(polygons, x, y):
    return [[tuple([point[0] + x, point[1] + y]) for point in polygon] for polygon in polygons]
