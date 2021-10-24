import cv2
import numpy as np
import matplotlib.pyplot as plt
import serial
import time

ArduinoSerial = serial.Serial('com4', 9600)
time.sleep(2)
print(ArduinoSerial.readline())


def make_coordinates(image, line_param):
    slope, intercetp = line_param
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercetp) / slope)
    x2 = int((y2 - intercetp) / slope)

    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        param = np.polyfit((x1, x2), (y1, y2), 1)

        slope = param[0]
        intercept = param[1]

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)

    mid = int((right_line[0] + left_line[0]) / 2)

    blue = (255, 0, 0)
    green = (0, 255, 0)
    bx1, by1, bx2, by2 = mid, 680, mid, 720
    gx1, gy1, gx2, gy2 = 640, 700, 640, 720
    mid_line = cv2.line(image, (bx1, by1), (bx2, by2), blue, 5)
    # distance_line = cv2.line(image, (gx1, gy1), (gx2, gy2), green, 2)

    # print("right: ", right_line[0])
    # print("left: ", left_line[0])
    # print("mid: ", bx1)

    left_distance = gx1 - left_line[0]
    right_distance = right_line[0] - gx1
    general_distance = left_distance - right_distance
    # print("Left_Distance: ", left_distance)
    # print("Right_Distance: ", right_distance)

    if general_distance < 0:
        general_distance = general_distance * (-1)

    if (left_distance > right_distance) and (general_distance > 100):
        print("Left")
        ArduinoSerial.write(b'0')

    elif (right_distance > left_distance) and (general_distance > 100):
        print("Right")
        ArduinoSerial.write(b'1')

    else:
        print("Straight")
        ArduinoSerial.write(b'2')

    return np.array([left_line, right_line])


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def region_of_interest(image):
    heihgt = image.shape[0]
    polygons = np.array([
        [(200, heihgt), (1100, heihgt), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image


# image = cv2.imread("car_view.PNG")
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# averaged_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# cv2.imshow("result", combo_image)
# cv2.waitKey(0)

cap = cv2.VideoCapture("test2.mp4")

while (cap.isOpened()):

    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", combo_image)
    key = cv2.waitKey(30)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()

