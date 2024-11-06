import sys
import time
from typing import Tuple, List
from abc import ABC

import cv2
import numpy as np

from main.config.parse_layouts import read_from_file
from main.led_char_map import LedCharMap
import os


class IElementSvg(ABC):

    def set_color(self, color):
        pass

    @property
    def svg_text(self):
        pass

    @property
    def led_number(self):
        pass


class SVGLedText(IElementSvg):
    def __init__(self, led_number: int, status: False, letter: str, x_pos: float, y_pos: float):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._led_number = led_number
        self._status = status

        self._color = (255, 255, 255)
        self._letter: str = letter
        self._font_family = "Ruler Stencil"
        self._font_size = 21

    def set_color(self, color):
        self._color = color

    @property
    def led_number(self):
        return self._led_number

    @property
    def svg_text(self):
        text = f"\t<text id = '{self.led_number}' x='{self._x_pos}' y ='{self._y_pos}' \n" \
               f"font-family='{self._font_family}' font-style= 'normal' font-weight='normal' \n" \
               f"fill='rgb{self._color}' font-size='{self._font_size}' text-anchor='middle' >{self._letter}</text>\n"
        return text


class SVGLedCorner(IElementSvg):
    def __init__(self, led_number: int, status: False, radius: int, x_pos: int, y_pos: int):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._led_number = led_number
        self._status = status

        self._color: Tuple = (255, 255, 255)
        self._radius: int = radius

    def set_color(self, color: Tuple):
        self._color = color

    @property
    def led_number(self):
        return self._led_number

    @property
    def svg_text(self):
        circle = f"\t<circle fill='rgb{self._color}' r='{self._radius}' cy='{self._x_pos}' cx='{self._y_pos}' />\n"
        return circle


class SVGWordclock:
    def __init__(self, leds: List[IElementSvg], bg_color: Tuple = (0, 0, 0),
                 height: int = 460, width: int = 460):
        self._height = height
        self._width = width
        self._bg_color = bg_color
        self._leds = leds
        self._svg_list = []

        # create basic layout with all leds white
        self._update_svg_text()

    def turn_all_led_off(self):
        for svg_led in self._leds:
            svg_led.set_color((20, 20, 20))

        self._update_svg_text()

    def turn_leds_on(self, led_numbers: List[int], color: Tuple):
        for led_number in led_numbers:
            for svg_led in self._leds:
                if svg_led.led_number == led_number:
                    svg_led.set_color(color)

        self._update_svg_text()

    def turn_led_on(self, led_number: int, color: Tuple):
        for svg_led in self._leds:
            if svg_led.led_number == led_number:
                svg_led.set_color(color)

        self._update_svg_text()

    @property
    def to_bytearray(self):
        return bytearray(self.__str__(), encoding="utf-8")
        # import io
        # from svglib.svglib import svg2rlg
        # from reportlab.graphics import renderPDF, renderPM
        #
        # svg_io = io.StringIO(self.__str__())
        # drawing = svg2rlg(svg_io)
        #
        # str = drawing.asString("png")
        # import pygame
        # test = pygame.image.fromstring(str.values(), (460, 460), "RGB")

        # test = pygame.image.load(str)
        # buff = io.BytesIO(str)
        # data = buff.getvalue()
        # return test

    def save(self, path: str):
        """
        Saves the SVG drawing to specified path.
        Let any exceptions propagate up to calling code.
        """
        try:
            f = open(path, "w", encoding="utf-8")
            text = str(self)
            f.write(text)
            f.close()

        except IOError as e:
            raise IOError(e)

    def _update_svg_text(self):
        self._svg_list.clear()
        for svg_led in self._leds:
            self._add_to_svg(svg_led.svg_text)

    def _add_to_svg(self, text):
        """
        Utility function to add element to drawing.
        """

        self._svg_list.append(str(text))

    @property
    def _background(self):
        rectangle = f"\t<rect fill='rgb{self._bg_color}' width='{self._width}' height='{self._height}' \n" \
                    f"y='0' x='0' ry='0' rx='0' />\n "

        return rectangle

    @property
    def _definitions(self):
        font_path = r"C:\git\wordclock_pi\source\font\ruler-stencil\Ruler Stencil Regular.ttf"
        devs = "<style> \n" \
               "@font-face { \n" \
               "font-family: font; \n" \
               f"src: url({font_path});\n" \
               "} \n" \
               "svg{\n" \
               "font-family: font, fallBackFonts, sans-serif;\n" \
               "} \n" \
               "</style>\n"

        return devs

    @property
    def _opening(self):
        """
        Adds the necessary opening element to document.
        """

        create = f"<svg width='{self._width}mm' height='{self._height}mm' viewBox='0 0 {self._width} {self._height}' xmlns='http://www.w3.org/2000/svg' version='1.2'>\n"

        return create

    @property
    def _finalize(self):
        """
        Closes the SVG element.
        """
        finalize = "</svg>"
        return finalize

    def __str__(self):
        """
        Returns the entire drawing by joining list elements.
        """
        content = "".join(self._svg_list)
        # svg = self._opening + self._definitions + self._background + content + self._finalize
        svg = self._opening + self._background + content + self._finalize
        return svg


def create_wordclock(layout_config) -> SVGWordclock:
    led_per_meter = 30
    led_delta_x = 1000 / led_per_meter
    led_delta_y = 34

    led_char_map = LedCharMap(layout_config=layout_config)

    n_cols = layout_config.info.columns_count
    n_rows = layout_config.info.rows_count

    corner_dist_edge = 20
    corner_dist = 460 - (2 * corner_dist_edge)

    start_x = (460 - (led_delta_x * (n_cols - 1))) / 2
    start_y = (460 - (led_delta_y * (n_rows - 1))) / 2

    leds = []
    for y_idx in range(0, n_rows):
        y_pos = start_y + y_idx * led_delta_y
        for x_idx in range(0, n_cols):
            x_pos = start_x + x_idx * led_delta_x
            letter = led_char_map.letter_matrix[y_idx, x_idx]
            id = int(led_char_map.led_number_matrix[y_idx, x_idx])
            led = SVGLedText(led_number=id, status=False, letter=letter, x_pos=x_pos, y_pos=y_pos)
            leds.append(led)

    # create corner leds

    leds.append(SVGLedCorner(led_number=200, status=False, radius=2,
                             x_pos=corner_dist_edge,
                             y_pos=corner_dist_edge))
    leds.append(SVGLedCorner(led_number=201, status=False, radius=2,
                             x_pos=corner_dist_edge + corner_dist,
                             y_pos=corner_dist_edge))
    leds.append(SVGLedCorner(led_number=202, status=False, radius=2,
                             x_pos=corner_dist_edge,
                             y_pos=corner_dist_edge + corner_dist))
    leds.append(SVGLedCorner(led_number=203, status=False, radius=2,
                             x_pos=corner_dist_edge + corner_dist,
                             y_pos=corner_dist_edge + corner_dist))

    wordclock = SVGWordclock(leds=leds)

    return wordclock


config_path = os.path.join(os.getcwd(), "..\\main\\config\\layouts.json")
layout_configs = read_from_file(config_path)
layout_config = layout_configs[0]
wordclock = create_wordclock(layout_config)
wordclock.save("simulator.svg")

from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QMainWindow
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Worker(QThread):
    svg_update = QtCore.pyqtSignal(bytearray)

    def __init__(self, myvar, parent=None):
        QThread.__init__(self, parent)
        self.myvar: SVGWordclock = myvar

    def run(self):
        """Long-running task."""
        for i in range(50):
            time.sleep(0.1)
            # Add svg widget
            self.myvar.turn_led_on(led_number=i, color=(255, 0, 0))
            svg_bytes = self.myvar.to_bytearray
            print(svg_bytes)
            self.svg_update.emit(svg_bytes)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        # QFrame / BG
        self.bg = QFrame()
        self.bg.setStyleSheet("background-color: #333")
        self.bg_layout = QVBoxLayout(self.bg)

        # Add svg widget
        self.wordclock: SVGWordclock = create_wordclock(layout_config)
        svg_bytes = self.wordclock.to_bytearray

        self.svg_widget = QSvgWidget()
        self.svg_widget.renderer().load(svg_bytes)
        self.svg_widget.setFixedSize(700, 700)

        # add svg to layout
        self.bg_layout.addWidget(self.svg_widget)

        # set central widget
        self.setCentralWidget(self.bg)

        self.start_rainbow_loop()

    def start_rainbow_loop(self):
        # Step 2: Create a QThread object
        self.thread = Worker(self.wordclock)
        self.thread.svg_update.connect(self.update_svg_widget)
        self.thread.start()

    def update_svg_widget(self, svg_bytes):
        self.svg_widget.renderer().load(svg_bytes)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

# i = 10

# while True:
#     cv2.imshow("image", res)
#     k = cv2.waitKey(1) & 0XFF
#     wordclock.turn_led_on(led_number=i, color=(255, 0, 0))
#     png_io = wordclock.to_byte_io_png()
#
#     decoded = cv2.imdecode(np.frombuffer(png_io, np.uint8), -1)
#     res = cv2.resize(decoded, dsize=(800, 800), interpolation=cv2.INTER_CUBIC)
#     i = i + 1
#     print(i)
#     if k == 27:
#         break

# cv2.destroyAllWindows()
