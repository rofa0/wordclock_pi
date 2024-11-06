from main.config.models.layout_config_definition import LayoutConfigDefinition
from main.config.models.layout_config_info import LayoutConfigInfo


class LayoutConfig:
    def __init__(self, layout_config_info: LayoutConfigInfo,
                 layout_config_definition: LayoutConfigDefinition):
        self._layout_config_info: LayoutConfigInfo = layout_config_info
        self._layout_config_definition: LayoutConfigDefinition = layout_config_definition

    @property
    def info(self) -> LayoutConfigInfo:
        return self._layout_config_info

    @property
    def definition(self) -> LayoutConfigDefinition:
        return self._layout_config_definition
