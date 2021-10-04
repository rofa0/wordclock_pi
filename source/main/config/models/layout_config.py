from typing import Dict
from main.models.layout_config_info import LayoutConfigInfo
from main.models.layout_config_definition import LayoutConfigDefinition


class LayoutConfig:
    def __init__(self, layout_config_info: LayoutConfigInfo,
                 layout_config_definition: LayoutConfigDefinition):
        self._layout_config_info: LayoutConfigInfo = layout_config_info
        self._layout_config_definition: LayoutConfigDefinition = layout_config_definition

    @property
    def config_info(self):
        return self._layout_config_info

    @property
    def config_definition(self):
        return self._layout_config_definition
