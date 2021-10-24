import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("car_view.PNG")


bx1, lx1, rx1 = 642, 270, 970
by1, ly1, ry1 = 680, 723, 723
bx2, lx2, rx2 = 642, 470, 780
by2, ly2, ry2 = 723, 560, 560

blue = (255, 0, 0)
blue_line = cv2.line(image, (bx1, by1), (bx2, by2), blue, 5)
left_line = cv2.line(image, (lx1, ly1), (lx2, ly2), blue, 5)
right_line = cv2.line(image, (rx1, ry1), (rx2, ry2), blue, 5)

left_distance = bx1 - lx1
right_distance = rx1 - bx1

# print("Sol Uzaklık : ", left_distance)
# print("Sağ Uzaklık : ", right_distance)

if left_distance > right_distance:
    print("Left")
else:
    print("Right")

plt.imshow(image)
plt.show()