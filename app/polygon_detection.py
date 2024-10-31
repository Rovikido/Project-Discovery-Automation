import cv2
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

import app.polygon_expander as pge
from app.utility.utility import get_centroid_of_polygon, polygon_contains_polygon


def draw_contours(image, min_area=150):
    """
    Detects contours in the given image and draws them.

    Parameters:
        image (numpy.ndarray): Input image.

    Returns:
        list: List of contours.
        numpy.ndarray: Image with drawn contours.
    """
    initial_contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = []
    for contour in initial_contours:
        contour = cv2.approxPolyDP(contour, 8, True)
        area = cv2.contourArea(contour)
        if min_area is not None and area < min_area:
            continue
        
        contours.append(contour)

    image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
    return contours, image_with_contours


def remove_blob_pixels(image, blockSize=821, min_blob_size=600, min_blob_area=400):
    """
    Removes blobs from the image based on size criteria.

    Parameters:
        image (numpy.ndarray): Input image.
        blockSize (int): Block size for GaussianBlur.
        min_blob_size (int): Minimum size of blobs to be considered.
        min_blob_area (int): Minimum area of blobs to be considered.

    Returns:
        numpy.ndarray: Image with blobs removed.
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) # Otsu's thresholding
    binary_image = 255 - binary_image
    i_height, i_width = image.shape

    blob_label = 1
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
    for i in range(1, num_labels):  # Skip background label (0)
        area = stats[i, cv2.CC_STAT_AREA]
        centroid = centroids[i]
        x, y, w, h = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]

        if area >= min_blob_area:
            print(f"Blob {i}: Area={area}, Centroid={centroid}, Bounding Box={(x, y, w, h)}")
            if  w == i_width and h == i_height:
                blob_label = i
                break
    # Create mask for the specified blob label
    blob_mask = np.zeros_like(binary_image)
    blob_mask[labels == blob_label] = 255
    blob_mask = cv2.bitwise_not(blob_mask)
    # blob_mask = erode_mask_least_bright(blob_mask, binary_image, increase_by=5, remove_at_least=40)
    blob_mask, image = check_for_countor_number(image, binary_image, blob_mask, itterations=10)

    result_image = cv2.bitwise_and(image, image, mask=blob_mask)
    return result_image


def erode_mask_least_bright(blob_mask, image, increase_by=5, remove_at_least=40):
    contours, _ = cv2.findContours(blob_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    kernel = np.ones((3, 3), np.uint8)
    eroded_mask = cv2.erode(blob_mask, kernel, iterations=increase_by)
    
    cv2.drawContours(eroded_mask, contours[0], 0, 255, thickness=cv2.FILLED)

    min_brightness = 255
    for y in range(eroded_mask.shape[0]):
        if min_brightness < remove_at_least:
            min_brightness = remove_at_least
            break
        for x in range(eroded_mask.shape[1]):
            if eroded_mask[y, x] == 0 and blob_mask[y, x] == 255:
                brightness = image[y, x]
                if brightness < min_brightness:
                    min_brightness = brightness
                
    blob_mask[image < min_brightness] = 0
    return cv2.bitwise_or(blob_mask, eroded_mask)


def check_for_countor_number(image, binary_image, blob_mask, itterations=3):
    updated_blob_mask = blob_mask.copy()
    contours, _ = draw_contours(cv2.bitwise_and(image, image, mask=updated_blob_mask))
    
    for i in range(itterations):
        # print(len(contours))
        if len(contours) != 1:
            return updated_blob_mask, image
        new_blob_mask = erode_mask_least_bright(updated_blob_mask, binary_image, increase_by=5, remove_at_least=40+i*20)
        new_contours, _ = draw_contours(cv2.bitwise_and(image, image, mask=updated_blob_mask))
        if len(new_contours) == 0:
            break
        contours = new_contours
        updated_blob_mask = new_blob_mask
    
    if len(contours)>=2:
        return updated_blob_mask, image

    if len(contours) == 1:
        new_blob_mask = updated_blob_mask.copy()
        contour = contours[0]
        height, width = blob_mask.shape[:2]
        opposite_contour = contour.copy()
        for point in opposite_contour:
            x, y = point[0]
            x = width - x
            y = height - y
            point[0] = [x, y]

        new_image = image.copy()
        # print(contour)
        old_contour = contour.copy()
        cv2.drawContours(new_blob_mask, [opposite_contour], 0, 255, thickness=cv2.FILLED)
        cv2.drawContours(new_image, [opposite_contour], 0, 255, thickness=cv2.FILLED)

        new_contours, _ = draw_contours(cv2.bitwise_and(new_image, new_image, mask=new_blob_mask))
        # print(len(new_contours))
        if True: # len(new_contours) == 1
            contour = [p[0] for p in contour]
            center = get_centroid_of_polygon(contour, round_=True)
            # print(center)
            add_x = 0
            add_y = 0
            if abs(image.shape[0]/2 - center[0]) < 10:
                add_x = -40 if (image.shape[0]/2 - center[0]) > 0 else 40
            if abs(image.shape[1]/2 - center[1]) < 10:
                add_y = -40 if (image.shape[1]/2 - center[1]) > 0 else 40
            opposite_contour = np.array([[[width - center[0]+9 + add_x, height - center[1] + add_y]],
                                [[width - center[0] + add_x, height - center[1]-9 + add_y]],
                                [[width - center[0]-9 + add_x, height - center[1] + add_y]],
                                [[width - center[0] + add_x, height - center[1]+9 + add_y]]
                                ])
            contour = np.array([[[center[0]+9 - add_x, center[1] - add_y]],
                                [[center[0] - add_x, center[1]-9 - add_y]],
                                [[center[0]-9 - add_x, center[1] - add_y]],
                                [[center[0] - add_x, center[1]+9 - add_y]]
                                ])


            new_image = image.copy()
            new_blob_mask = updated_blob_mask.copy()
            # print(contour)
            cv2.drawContours(new_blob_mask, [opposite_contour], 0, 255, thickness=cv2.FILLED)
            cv2.drawContours(new_image, [opposite_contour], 0, 255, thickness=cv2.FILLED)

            cv2.drawContours(new_blob_mask, [contour], 0, 255, thickness=cv2.FILLED)
            cv2.drawContours(new_image, [contour], 0, 255, thickness=cv2.FILLED)

            new_contours, _ = draw_contours(cv2.bitwise_and(new_image, new_image, mask=new_blob_mask))
            if len(new_contours) == 0:
                cv2.drawContours(updated_blob_mask, [old_contour], 0, 255, thickness=cv2.FILLED)
                cv2.drawContours(image, [old_contour], 0, 255, thickness=cv2.FILLED)
                return updated_blob_mask, image

        updated_blob_mask[:] = 0
        image[:, :] = 0
        cv2.drawContours(updated_blob_mask, [opposite_contour], 0, 255, thickness=cv2.FILLED)
        cv2.drawContours(image, [opposite_contour], 0, 255, thickness=cv2.FILLED)

        cv2.drawContours(updated_blob_mask, [contour], 0, 255, thickness=cv2.FILLED)
        cv2.drawContours(image, [contour], 0, 255, thickness=cv2.FILLED)
    

    return updated_blob_mask, image


def downscale_hue(hsv_image, scale_factor):
    h, s, v = cv2.split(hsv_image)
    downscaled_hue = cv2.resize(h, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    downscaled_saturation = cv2.resize(s, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    downscaled_value = cv2.resize(v, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    downscaled_hsv_image = cv2.merge([downscaled_hue, downscaled_saturation, downscaled_value])
    return downscaled_hsv_image


def replace_color_with_black(image, color_to_replace, n=5):
    b, g, r = cv2.split(image)

    # Define the range for each color channel
    lower_bound = np.array([color_to_replace[0] - n, color_to_replace[1] - n, color_to_replace[2] - n])
    upper_bound = np.array([color_to_replace[0] + n, color_to_replace[1] + n, color_to_replace[2] + n])

    # Create a mask for pixels within the specified color range
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Replace those pixels with black
    image[mask > 0] = [0, 0, 0]

    return image


def downscale_image_by_n(image, n):
    new_width = image.shape[1] // n
    new_height = image.shape[0] // n
    downscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return downscaled_image


def upscale_polygons(polygons, value):
    return [[[(cord * value) for cord in point] for point in polygon] for polygon in polygons]


def find_brightest_point(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray_image)
    return max_loc


def generate_random_polygons(image):
    height, width = image.shape[:2]
    center = find_brightest_point(image)
    add_x = 0
    add_y = 0
    if abs(image.shape[0]/2 - center[0]) < 10:
        add_x = -40 if (image.shape[0]/2 - center[0]) > 0 else 40
    if abs(image.shape[1]/2 - center[1]) < 10:
        add_y = -40 if (image.shape[1]/2 - center[1]) > 0 else 40
    res = [[[width - center[0]+9 + add_x, height - center[1] + add_y],
            [width - center[0] + add_x, height - center[1]-9 + add_y],
            [width - center[0]-9 + add_x, height - center[1] + add_y],
            [width - center[0] + add_x, height - center[1]+9 + add_y]],
            [[center[0] + 9 - add_x, center[1] - add_y],
            [center[0] - add_x, center[1] - 9 - add_y],
            [center[0] - 9 - add_x, center[1] - add_y],
            [center[0] - add_x, center[1] + 9 - add_y]]]
    return res


def get_polygons_from_image(image, downscale_by=2, debug=False):
    orginial_image=image.copy()
    try:
        image = replace_color_with_black(image, (40, 40, 40))
        image = downscale_image_by_n(image, downscale_by)
        image = remove_blob_pixels(image)

        if debug:
            cv2.imshow('Result', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        contours, image_with_contours = draw_contours(image)

        if debug:
            cv2.imshow("Image with Contours", image_with_contours)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


        contours = [[c[0] for c in cont] for cont in contours]

        polygons = pge.expand_polygons(contours, image.shape[:2])       
        
        polygons = upscale_polygons(polygons, downscale_by)

        if debug:
            contours = [np.array(polygon).reshape((-1, 1, 2)) for polygon in polygons]
            expanded_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            cv2.drawContours(expanded_image, contours, -1, (0, 255, 0), 2)
            cv2.imshow("Polygons Contours", expanded_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        polygons = [[tuple(point) for point in polygon] for polygon in polygons]

        for polygon1 in polygons:
            for polygon2 in polygons:
                if not polygon1 == polygon2:
                    if polygon_contains_polygon(polygon1=polygon1, polygon2=polygon2):
                        raise ValueError('Polygon contains other polygons points!')
    except Exception as e:
        print(e)
        polygons = generate_random_polygons(orginial_image)
        print(polygons)
        polygons = pge.expand_polygons(polygons, image.shape[:2])       
        polygons = upscale_polygons(polygons, downscale_by)
        polygons = [[tuple(point) for point in polygon] for polygon in polygons]
        return polygons

    return polygons


def gen_rand_polygons_interface(image, downscale_by=2, debug=False):
    orginial_image=image.copy()
    polygons = generate_random_polygons(orginial_image)
    polygons = pge.expand_polygons(polygons, image.shape[:2])       
    polygons = upscale_polygons(polygons, downscale_by)
    polygons = [[tuple(point) for point in polygon] for polygon in polygons]

    return polygons
