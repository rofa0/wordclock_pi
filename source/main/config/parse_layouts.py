import json
from pathlib import Path
from typing import List

from main.config.models.layout_config import LayoutConfig
from main.config.models.layout_config_definition import Corner, PanelLedCharMap
# config definition
from main.config.models.layout_config_definition import LayoutConfigDefinition
from main.config.models.layout_config_definition import TextDefinitionTime, TextDefinitionOther, TextDefinitionHour
# config info
from main.config.models.layout_config_info import LayoutConfigInfo


def read_from_file(file_path: Path) -> List[LayoutConfig]:
    with open(file_path, encoding='utf-8') as f:
        layout_dict = json.load(f)

    layouts = []
    for layout in layout_dict["layouts"]:
        info_dict = layout["info"]
        definition_dict = layout["definition"]

        info = _parse_info(info_dict=info_dict)
        definition = _parse_definition(definition_dict=definition_dict)

        layout_config = LayoutConfig(layout_config_info=info,
                                     layout_config_definition=definition)

        layouts.append(layout_config)
    return layouts


def _parse_info(info_dict) -> LayoutConfigInfo:
    info = LayoutConfigInfo(layout_info_dict=info_dict)
    return info


def _parse_definition(definition_dict) -> LayoutConfigDefinition:
    # create corners list
    corners = []
    for corner in definition_dict["corners"]:
        corners.append(Corner(corners_dict=corner))

    # create panel led char map
    panel_led_char_map = []
    for char_map in definition_dict["panel_led_char_map"]:
        panel_led_char_map.append(PanelLedCharMap(char_map_dict=char_map))

    # text definitions
    text_definitions = definition_dict["text_definitions"]

    # time
    time = TextDefinitionTime(text_definition_dict=text_definitions["time"])

    # other
    other = TextDefinitionOther(other_dict=text_definitions["other"])

    # hours
    hours = []
    for hour in text_definitions["hours"]:
        hours.append(TextDefinitionHour(hours_dict=hour))

    # create definition object
    definition = LayoutConfigDefinition(panel_led_char_map=panel_led_char_map,
                                        corners=corners,
                                        text_definition_time=time,
                                        text_definition_hours=hours,
                                        text_definition_other=other)

    return definition
