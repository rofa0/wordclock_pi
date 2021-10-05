import numpy as np
import cv2
from typing import List


class LedImage:
    def __init__(self, location_x: int,
                 location_y: int,
                 contours: List[np.ndarray],
                 empty_image: np.ndarray,
                 led_number: int,
                 led_char: str):
        self._loc_x: int = location_x
        self._loc_y: int = location_y
        self._contours: List[np.ndarray] = contours
        self._empty_image: np.ndarray = empty_image
        self._led_number: int = led_number
        self._led_char: str = led_char

        self._led_status = False

    @property
    def led_number(self):
        return self._led_number

    def off(self, image):
        shape = self._empty_image.shape
        # draw the contour with specific color to the empty letter or corner image
        cv2.drawContours(self._empty_image, self._contours, -1, (15, 15, 15), thickness=cv2.FILLED)
        # insert the led image to the provided image
        image[self._loc_x: self._loc_x + shape[0], self._loc_y:self._loc_y + shape[1]] = self._empty_image
        self._led_status = False
        # return the overlayed image
        return image

    def on(self, r, g, b, image):
        shape = self._empty_image.shape
        # draw the contour with specific color to the empty letter or corner image
        cv2.drawContours(self._empty_image, self._contours, -1, (b, g, r), thickness=cv2.FILLED)
        # insert the led image to the provided image
        image[self._loc_x: self._loc_x + shape[0], self._loc_y:self._loc_y + shape[1]] = self._empty_image
        self._led_status = True
        # return the overlayed image
        return image

    def __repr__(self):
        return f"LED: {self._led_char} , Number: {self._led_number}, Is On: {self._led_status}"
