import pyautogui
import cv2
import numpy as np
from time import sleep
import matplotlib.pyplot as plt


def get_screenshot_at(x=1084, y=311, w=448, h=416):
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    # cv2.imwrite('output_image5.jpg', cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR))
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)






# sleep(5)
# image = get_image()
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


# mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([100, 100, 50]))
# mask = cv2.bitwise_not(mask)
# hsv_new = cv2.bitwise_and(hsv, hsv, mask=mask)


# data_points = []

# height, width = hsv.shape[:2]
# for y in range(height):
#     for x in range(width):
#         color = hsv[y, x]
#         val = color_to_value(color)
#         if val <= 0:
#             hsv[y,x] = (0,0,0)
#             continue
#         hsv[y,x] = (val*240,100,100)
#         data_points.append((x, y, val))


# cv2.imshow('Segmented Image', hsv)
# cv2.waitKey(0)

# # Iterate over each color range
# for lower_color, upper_color in color_ranges:
#     mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

#     # Find contours
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Iterate through each contour
#     for contour in contours:
#         # Calculate moments of contour
#         M = cv2.moments(contour)
        
#         # Calculate the center of mass of the contour
#         if M["m00"] != 0:
#             cx = int(M["m10"] / M["m00"])
#             cy = int(M["m01"] / M["m00"])
#         else:
#             cx, cy = 0, 0
        
#         # Get the color of the point
#         color = image[cy, cx]

#         # Calculate the normalized value based on color intensity (assuming BGR)
#         value_normalized = (color[2] - 0) / (255 - 0)  # red channel intensity

#         # Add data point to the list
#         data_points.append((cx, cy, value_normalized))

# Extract x, y, and values from data points
# x_values = [point[0] for point in data_points]
# y_values = [point[1] for point in data_points]
# values = [point[2] for point in data_points]

# # Plot the data points
# plt.scatter(x_values, y_values, c=values, cmap='coolwarm', s=50, edgecolors='k')
# plt.colorbar(label='Normalized Value')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Data Points with Color Based on Normalized Value')
# plt.grid(True)
# plt.show()