from typing import Dict
from typing import List


class Corner:
    def __init__(self, corners_dict: Dict):
        self._dict = corners_dict

    @property
    def minute(self) -> int:
        return self._dict.get("minute")

    @property
    def led(self) -> int:
        return self._dict.get("led")


class PanelLedCharMap:
    def __init__(self, char_map_dict: Dict):
        self._dict = char_map_dict

    @property
    def row_number_from_top(self) -> int:
        return self._dict.get("row_number_from_top")

    @property
    def letters(self) -> str:
        return self._dict.get("letters")

    @property
    def left_led_number(self) -> int:
        return self._dict.get("left_led_number")

    @property
    def right_led_number(self) -> int:
        return self._dict.get("right_led_number")


class TextDefinitionTime:
    def __init__(self, text_definition_dict: Dict):
        self._dict = text_definition_dict

    @property
    def past(self):
        return self._dict.get("past")

    @property
    def to(self):
        return self._dict.get("to")

    @property
    def five(self):
        return self._dict.get("five")

    @property
    def ten(self):
        return self._dict.get("ten")

    @property
    def half(self):
        return self._dict.get("half")

    @property
    def twenty(self):
        return self._dict.get("twenty")

    @property
    def quarter(self):
        return self._dict.get("quarter")


class TextDefinitionOther:
    def __init__(self, other_dict: Dict):
        self._dict = other_dict

    @property
    def clock_text(self):
        return self._dict.get("clock")

    @property
    def it_text(self):
        return self._dict.get("it")

    @property
    def is_text(self):
        return self._dict.get("is")


class TextDefinitionHour:
    def __init__(self, hours_dict: Dict):
        self._dict = hours_dict

    @property
    def hour(self) -> int:
        return self._dict.get("hour")

    @property
    def letters(self) -> str:
        return self._dict.get("letters")


class LayoutConfigDefinition:
    def __init__(self, panel_led_char_map: List[PanelLedCharMap],
                 corners: List[Corner],
                 text_definition_time: TextDefinitionTime,
                 text_definition_other: TextDefinitionOther,
                 text_definition_hours: List[TextDefinitionHour]):
        self._panel_led_char_map: List[PanelLedCharMap] = panel_led_char_map
        self._corners: List[Corner] = corners
        self._text_definition_time: TextDefinitionTime = text_definition_time
        self._text_definition_other: TextDefinitionOther = text_definition_other
        self._text_definition_hours: List[TextDefinitionHour] = text_definition_hours

    @property
    def panel_led_char_map(self):
        return self._panel_led_char_map

    @property
    def corners(self):
        return self._corners

    @property
    def text_definition_time(self):
        return self._text_definition_time

    @property
    def text_definition_other(self):
        return self._text_definition_other

    @property
    def text_definition_hours(self):
        return self._text_definition_hours
