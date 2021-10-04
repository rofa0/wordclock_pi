from typing import Dict


class LayoutConfigDefinition:
    def __init__(self, layout_definition_dict: Dict):
        self._dict: Dict = layout_definition_dict

    @property
    def panel_led_char_map(self) -> str:
        return self._dict.get("panel_led_char_map")

    @property
    def corners(self) -> str:
        return self._dict.get("corners")

    @property
    def text_definitions(self) -> str:
        return self._dict.get("text_definitions")
