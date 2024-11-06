from datetime import datetime

import numpy as np
import numpy.ma as ma

import os
from main.config.parse_layouts import read_from_file
from main.led_char_map import LedCharMap
from simulator.led_image import LedImage

# image processing
import cv2

import numpy as np
import matplotlib.pyplot as plt


def get_leds(time: datetime, led_char_map):
    hour = time.hour
    minute = time.minute
    leds_on = []
    # Round minute to the nearest 5
    minute_round = (minute // 5) * 5

    # If the minute is greater than 20, increment the hour
    if minute_round > 20:
        hour += 1

    # Adjust for 12-hour format (word clock often uses 12 hours)
    if hour > 12:
        hour -= 12
    elif hour == 0:
        hour = 12

    # Add LEDs for the hour
    if hour in led_char_map.hours:
        leds_on.extend(led_char_map.hours[hour])

    # Add LEDs for the rounded minute
    if minute_round != 0 and minute_round in led_char_map.minutes:
        leds_on.extend(led_char_map.minutes[minute_round])

    # Calculate additional minutes after the nearest 5-minute rounding
    additional_minutes = minute % 5
    if additional_minutes > 0:
        # Use `led_char_map.corners` to add the appropriate corner LED
        if additional_minutes in led_char_map.corners.keys():
            leds_on.append(led_char_map.corners[additional_minutes])

    return leds_on  # List of LED numbers


def simulate_wordclock(hour, minute):
    led_map_copy = np.copy(led_char_map.led_number_matrix)
    for value in get_leds(hour, minute):
        led_map_copy[led_map_copy == value] = "0"
    c = ma.masked_where(led_map_copy != 0, led_char_map.letter_matrix)
    return (c)


def ndtotext(A, w=None, h=None):
    """
    pretty print np.ndarray
    """
    if A.ndim == 1:
        if w == None:
            return str(A)
        else:
            s = '[' + ' ' * (max(w[-1], len(str(A[0]))) - len(str(A[0]))) + str(A[0])
            for i, AA in enumerate(A[1:]):
                s += ' ' * (max(w[i], len(str(AA))) - len(str(AA)) + 1) + str(AA)
            s += '] '
    elif A.ndim == 2:
        w1 = [max([len(str(s)) for s in A[:, i]]) for i in range(A.shape[1])]
        w0 = sum(w1) + len(w1) + 1
        s = u'\u250c' + u'\u2500' * w0 + u'\u2510' + '\n'
        for AA in A:
            s += ' ' + ndtotext(AA, w=w1) + '\n'
        s += u'\u2514' + u'\u2500' * w0 + u'\u2518'
    elif A.ndim == 3:
        h = A.shape[1]
        s1 = u'\u250c' + '\n' + (u'\u2502' + '\n') * h + u'\u2514' + '\n'
        s2 = u'\u2510' + '\n' + (u'\u2502' + '\n') * h + u'\u2518' + '\n'
        strings = [ndtotext(a) + '\n' for a in A]
        strings.append(s2)
        strings.insert(0, s1)
        s = '\n'.join(''.join(pair) for pair in zip(*map(str.splitlines, strings)))
    return s


############# image processing ###################
def simple_edge_detection(image):
    edges_detected = cv2.Canny(image, 100, 200)
    images = [image, edges_detected]
    return images


if __name__ == "__main__":
    config_path = os.path.join(os.getcwd(), "..\\main\\config\\layouts.json")
    front_image = os.path.join(os.getcwd(), "..\\simulator\\image\\front_swissgerman.png")

    layout_configs = read_from_file(config_path)
    layout_config = layout_configs[0]
    led_char_map = LedCharMap(layout_config=layout_config)

    img = cv2.imread(front_image, cv2.IMREAD_UNCHANGED)

    # restrict contours
    print(img.shape)
    height, width = img.shape[:2]

    widthMax = width / 10
    heightMax = height / 10

    contours_filt = []

    clock_width_mm = 460
    clock_height_mm = 460

    factor_pixel_mm = width / clock_width_mm

    clock_width_pixel = clock_width_mm * factor_pixel_mm
    clock_height_pixel = clock_height_mm * factor_pixel_mm

    raster_width_mm = 33.33
    raster_height_mm = 36

    raster_width_pixel = raster_width_mm * factor_pixel_mm
    raster_height_pixel = raster_height_mm * factor_pixel_mm

    raster_x_count = int(clock_width_mm / raster_width_mm)
    raster_y_count = int(clock_height_mm / raster_height_mm)

    delta_x_mm = (clock_width_mm - raster_x_count * raster_width_mm) / 2
    delta_y_mm = (clock_height_mm - raster_y_count * raster_height_mm) / 2

    delta_x_pixel = delta_x_mm * factor_pixel_mm
    delta_y_pixel = delta_y_mm * factor_pixel_mm

    print(delta_x_mm, delta_x_pixel)

    # create raster x coordinates
    raster_x_coordinates = []
    sum = delta_x_pixel + raster_width_pixel
    for x in range(raster_x_count - 2):
        raster_x_coordinates.append(sum)
        sum += raster_width_pixel

    # create raster y coordinates
    raster_y_coordinates = []
    sum = delta_y_pixel + raster_height_pixel
    for y in range(raster_y_count - 2):
        raster_y_coordinates.append(sum)
        sum += raster_height_pixel

    led_images = []
    # loop over y coordinates
    for idx_y, y_cord in enumerate(raster_y_coordinates):
        y_max = int(y_cord + raster_height_pixel)
        y_min = int(y_cord)

        # loop over x coordinates
        for idx_x, x_cord in enumerate(raster_x_coordinates):
            x_max = int(x_cord + raster_width_pixel)
            x_min = int(x_cord)

            crop_img = img[y_min:y_max, x_min:x_max]

            # convert img to grey
            img_grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            # set a thresh
            thresh = 150
            # get threshold image
            ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
            # find contours
            contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours_filtered = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                width_max = (x_max - x_min) * 0.8  # treshold to 80 percent of total width
                height_max = (y_max - y_min) * 0.8
                if (w < width_max) and (h < height_max):
                    contours_filtered.append(cnt)

            if contours_filtered:
                # create an empty image for contours
                empty_image = np.zeros(crop_img.shape)
                led_image = LedImage(location_x=y_min,
                                     location_y=x_min,
                                     contours=contours_filtered,
                                     empty_image=empty_image,
                                     led_number=led_char_map.led_number_matrix[idx_y, idx_x],
                                     led_char=led_char_map.letter_matrix[idx_y, idx_x])

                led_images.append(led_image)

    # led_image = led_images[20]
    # img = led_image.show(r=255, g=0, b=0, image=img)
    # print(led_image)

    leds = get_leds(hour=datetime.datetime.now().hour,
                    minute=datetime.datetime.now().minute)

    for led_image in led_images:
        if led_image.led_number in leds:
            img = led_image.on(r=255, g=0, b=0, image=img)
            print(led_image)
        else:
            img = led_image.off(image=img)
            print(led_image)

    # sim_time = []
    # for hour in range(0, 24):
    #     for minute in range(0, 60):
    #         display = "{:02d}:{:02d}".format(hour, minute)
    #
    #         clock = simulate_wordclock(hour, minute)
    #         sim_time.append([display, clock])
    #         print(display)
    #         print(ndtotext(clock))
    #         print("")
    #         print("")

    cv2.imshow("Roger's Wordclock Simulator", img)
    cv2.waitKey(0)
    # # closing all open windows
    cv2.destroyAllWindows()

    # for i in range(0,110):
    #     color = (15,15,15)
    #
    #     index = i
    #     contours = test[index][0]
    #     empty_image = test[index][2]
    #     loc = test[index][1]
    #     x_min = loc[0]
    #     x_max = loc[1]
    #     y_min = loc[2]
    #     y_max = loc[3]
    #
    #     shape = empty_image.shape
    #     cv2.drawContours(empty_image, contours, -1, color, thickness=cv2.FILLED)
    #
    #     img[x_min: x_min + shape[0], y_min:y_min + shape[1]] = empty_image
    #
    # cv2.imshow("Test", img)
    # cv2.waitKey(0)
    # # # closing all open windows
    # cv2.destroyAllWindows()
    #
    # breakpoint()
    #
    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #
    #     rect = cv2.minAreaRect(cnt)  # I have used min Area rect for better result
    #     width = rect[1][0]
    #     height = rect[1][1]
    #
    #     if (width < widthMax) and (height < heightMax) and (x > x_max) and (x < x_min):
    #         contours_filt.append(cnt)
    #         print(x, y)
    #
    # # create an empty image for contours
    # img_contours = np.zeros(img.shape)
    # # draw the contours on the empty image
    # rgb = (255, 0, 0)
    # cv2.drawContours(img_contours, contours, -1, rgb, thickness=cv2.FILLED)
    #
    # cv2.imshow("Test", img_contours)
    # # waits for user to press any key
    # # (this is necessary to avoid Python kernel form crashing)
    # cv2.waitKey(0)
    #
    # # closing all open windows
    # cv2.destroyAllWindows()
    # #
    #

