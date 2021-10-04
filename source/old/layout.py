from typing import List


class Text:
    def __init__(self, text: str, leds: List[int]):
        self._text: str = text
        self._leds: List[int] = leds

    @property
    def text(self) -> str:
        return self._text

    @property
    def leds(self) -> List[int]:
        return self._leds


class Ecke:
    def __init__(self, minute: int, led: int):
        self._minute: int = minute
        self._led: int = led

    @property
    def minute(self) -> int:
        return self._minute

    @property
    def led(self) -> int:
        return self._led


class Stunde:
    def __init__(self, stunde: int, leds: List[int]):
        self._stunde: int = stunde
        self._leds: List[int] = leds

    @property
    def stunde(self) -> int:
        return self._stunde

    @property
    def leds(self) -> List[int]:
        return self._leds




class Layout:
    """
    =========================================================================================//
                                              LED Layout                                     //
    =========================================================================================//
      112                                                                               111

           100/E  101/S  102/K  103/I  104/S  105/C  106/H  107/A  108/F  109/Ü  110/F
           99/V   98/I   97/E   96/R   95/T   94/U   93/B   92/F   91/Z   90/Ä   89/Ä
           78/Z   79/W   80/Ä   81/N   82/Z   83/G   84/S   85/I   86/V   87/O   88/R
           77/A   76/B   75/O   74/H   73/A   72/U   71/B   70/I   69/E   68/G   67/E
           56/E   57/I   58/S   59/Z   60/W   61/Ö   62/I   63/S   64/D   65/R   66/Ü
           55/V   54/I   53/E   52/R   51/I   50/F   49/Ü   48/F   47/I    46/Q   45/T
           34/S   35/Ä   36/C   37/H   38/S   39/I   40/S   41/I   42/B   43/N   44/I
           33/A   32/C   31/H   30/T   29/I   28/N   27/Ü   26/N   25/I   24/E   23/L
           12/Z   13/Ä   14/N   15/I   16/E   17/R   18/B   19/Ö   20/U   21/F   22/I
           11/Z   10/W   9/Ö    8/U    7/F    6/I    5/N    4/A    3/U    2/H    1/R

      113                                                                                0
     """

    def __init__(self, layout_config):
        self._text_config: List = layout_config["text_definition"]
        self._ecken_config: List = layout_config["corners"]
        self._stunden_config: List = layout_config["hours"]

    def _get_leds_from_text(self, strings: List[str]) -> List[int]:
        leds = []
        for text in strings:
            for element in self._text_config:
                if text == element["text"]:
                    leds.insert(element["leds"])
        return leds

    @property
    def text(self) -> List[Text]:
        text_config_list = []
        for element in self._text_config:
            text = element["text"]
            leds = element["leds"]

            text = Text(text=text, leds=leds)
            text_config_list.append(text)
        return text_config_list

    @property
    def ecken(self) -> List[Ecke]:
        ecke_conifg_list = []
        for element in self._ecken_config:
            minute = element["minute"]
            led = element["led"]
            ecke = Ecke(minute=minute, led=led)
            ecke_conifg_list.append(ecke)

        return ecke_conifg_list

    @property
    def stunden(self) -> List[Stunde]:
        stunde_conifg_list = []
        for element in self._stunden_config:
            stunde = element["stunde"]
            leds = element["leds"]
            stunde = Stunde(stunde=stunde, leds=leds)
            stunde_conifg_list.append(stunde)

        return stunde_conifg_list







#
#
# # Fünf Minuten Schritte
# nach = [77, 76]
# vor = [86, 87, 88]
# halb = [74, 73, 72, 71, 70]
# fünf = [108, 109, 110]
# zehn = [91, 90, 89]
# zwanzig = [78, 79, 80, 81, 82, 83]
# viertel = [94, 95, 96, 97, 98, 99]
#
# MINUTEN = {
#     5: fünf + nach,  # Fünf nach
#     10: zehn + nach,  # Zehn nach
#     15: viertel + nach,  # Viertel Nach
#     20: zwanzig + nach,  # Zwanzig nach"
#     25: fünf + vor + halb,  # Fünf vor halb
#     30: halb,  # Halb
#     35: fünf + nach + halb,  # Fünf nach Halb
#     40: zwanzig + vor,  # Zwanzig vor
#     45: viertel + vor,  # Viertel vor
#     50: zehn + vor,  # Zehn vor
#     55: fünf + vor,  # Fünf vor
# }
#
# # Stunden
# STUNDEN = {
#     1: [56, 57, 58],
#     2: [59, 60, 61, 62],
#     3: [64, 65, 66],
#     4: [55, 54, 53, 52, 51],
#     5: [50, 49, 48, 57],
#     6: [34, 35, 36, 37, 38, 39],
#     7: [40, 41, 42, 43, 44],
#     8: [29, 30, 31, 32, 33],
#     9: [28, 27, 26, 25],
#     10: [12, 13, 14, 15],
#     11: [19, 20, 21, 22],
#     12: [11, 10, 9, 8, 7, 6],
# }
#
# # Einzelne Minuten in den Ecken
# ECKEN = {
#     1: [111],
#     2: [111, 0],
#     3: [111, 0, 113],
#     4: [111, 0, 113, 112]
# }
#
# ES = [100, 101]
# IST = [103, 104, 105, 106]
# UHR = [3, 2, 1]
#
#
# class Minutes:
# def __init__(self):
#     # Fünf Minuten Schritte
#     nach = [77, 76]
#     vor = [86, 87, 88]
#     halb = [74, 73, 72, 71, 70]
#     fünf = [108, 109, 110]
#     zehn = [91, 90, 89]
#     zwanzig = [78, 79, 80, 81, 82, 83]
#     viertel = [94, 95, 96, 97, 98, 99]
