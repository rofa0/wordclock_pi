import datetime
from typing import List
import numpy as np
import os
import json
from main.layout import Layout
from main.config_parser import get_layout_config


def create_row_numbers(left, right):
    if left > right:
        step = -1
        numbers = [i for i in range(left, right - 1, step)]

    else:
        step = 1
        numbers = [i for i in range(left, right + 1, step)]

    return numbers


def create_letter_list(string):
    letters = [letter for letter in string]
    return letters


def create_2d_array(config):
    letters = []
    led_numbers = []
    for row in config["panel_led_char_map"]:
        chars = row["letters"]
        left_led_number = row["left_led_number"]
        right_led_number = row["right_led_number"]

        letters.append(create_letter_list(chars))
        led_numbers.append(create_row_numbers(left=left_led_number, right=right_led_number))

    array_letters = np.array(letters, dtype='U1')
    array_leds = np.array(led_numbers)

    return array_leds, array_letters


class Word:
    def __init__(self, text: str, leds: List[int]):
        self._text: str = text
        self._leds: List[int] = leds

    @property
    def text(self) -> str:
        return self._text

    @property
    def leds(self) -> List[int]:
        return self._leds


config = get_layout_config(filepath=os.path.join(os.getcwd(), "main\\layout_config.json"))
array_leds, array_letters = create_2d_array(config)


test = Layout(layout_config=config)

time = datetime.datetime.now()
hour = 12 if time.hour % 12 == 0 else time.hour % 12
minute_5min_step = time.minute - (time.minute % 5)
minute_corner = time.minute % 5

print(f"hour: {hour}")
print(f"minute: {minute_5min_step}")
print(f"corner: {minute_corner}")

breakpoint()
