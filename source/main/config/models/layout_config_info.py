from typing import Dict


class LayoutConfigInfo:
    def __init__(self, layout_info_dict: Dict):
        self._dict: Dict = layout_info_dict

    @property
    def language(self) -> str:
        return self._dict.get("language")

    @property
    def dialect(self) -> str:
        return self._dict.get("dialect")
