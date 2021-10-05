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

    @property
    def rows_count(self) -> int:
        return self._dict.get("rows_count")

    @property
    def columns_count(self) -> int:
        return self._dict.get("columns_count")
