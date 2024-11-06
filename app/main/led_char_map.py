from functools import cached_property

import numpy as np

from main.config.models.layout_config import LayoutConfig


class LedCharMap:
    def __init__(self, layout_config: LayoutConfig):
        self._layout: LayoutConfig = layout_config

    @cached_property
    def led_number_matrix(self) -> np.ndarray:
        led_numbers = []
        for row in self._layout.definition.panel_led_char_map:
            led_numbers.append(self._create_row_numbers(left=row.left_led_number, right=row.right_led_number))

        return np.array(led_numbers)

    @cached_property
    def letter_matrix(self):
        letters = []
        for row in self._layout.definition.panel_led_char_map:
            letters.append(self._create_letter_list(row.letters))

        return np.array(letters, dtype='U1')

    @cached_property
    def minutes(self) -> dict:
        past = self._find_leds_from_config(self._layout.definition.text_definition_time.past)
        to = self._find_leds_from_config(self._layout.definition.text_definition_time.to)
        five = self._find_leds_from_config(self._layout.definition.text_definition_time.five)
        ten = self._find_leds_from_config(self._layout.definition.text_definition_time.ten)
        quarter = self._find_leds_from_config(self._layout.definition.text_definition_time.quarter)
        twenty = self._find_leds_from_config(self._layout.definition.text_definition_time.twenty)
        half = self._find_leds_from_config(self._layout.definition.text_definition_time.half)

        minutes = {
            5: five + past,
            10: ten + past,
            15: quarter + past,
            20: twenty + past,
            25: five + to + half,
            30: half,
            35: five + past + half,
            40: twenty + to,
            45: quarter + to,
            50: ten + to,
            55: five + to,
        }
        return minutes

    @cached_property
    def hours(self) -> dict:
        hours = {}
        for hour in self._layout.definition.text_definition_hours:
            string = hour.letters
            # find led's corresponding to string
            leds = self._find_leds_from_config(string)
            # create dict entry for the specific hour
            hours[hour.hour] = leds
        return hours

    @cached_property
    def corners(self) -> dict:
        corners = {}
        for corner in self._layout.definition.corners:
            corners[corner.minute] = corner.led

        return corners

    @staticmethod
    def _create_letter_list(string):
        letters = [letter for letter in string]
        return letters

    @staticmethod
    def _create_row_numbers(left, right):
        if left > right:
            step = -1
            numbers = [i for i in range(left, right - 1, step)]

        else:
            step = 1
            numbers = [i for i in range(left, right + 1, step)]

        return numbers

    def _find_leds_from_config(self, search_string):
        for row in self._layout.definition.panel_led_char_map:
            if search_string in row.letters:
                index = row.letters.find(search_string)
                if row.right_led_number > row.left_led_number:
                    leds_row = list(range(row.left_led_number, row.right_led_number + 1))
                else:
                    leds_row = list(range(row.left_led_number, row.right_led_number - 1, -1))
                leds = leds_row[index: index + len(search_string)]
                return leds
