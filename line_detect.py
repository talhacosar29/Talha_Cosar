import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("car_view.PNG")

im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

masked_white = cv2.inRange(im, 155, 255)
blurred = cv2.GaussianBlur(masked_white, (5,5), 0.8)
edge_image = cv2.Canny(blurred, 50, 150)

mask = np.zeros_like(edge_image)
vertices = np.array([[(270, 700), (550, 500), (705, 487), (950, 700)]], np.int32)
#print(vertices)

cv2.fillPoly(mask, vertices, 255)

#print(edge_image.shape, mask.shape)
masked = cv2.bitwise_and(edge_image, mask)

lines = cv2.HoughLinesP(masked, 2, np.pi/180, 20, np.array([]), minLineLength=50, maxLineGap= 200)
zeros = np.zeros_like(image)

for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(zeros, (x1, y1), (x2, y2), (0, 255, 0), 5)

image = cv2.addWeighted(image, 0.8, zeros, 1.0, 0.)

plt.imshow(image)
plt.show()
