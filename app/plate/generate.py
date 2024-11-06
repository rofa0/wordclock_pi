import base64
import os
from datetime import datetime

import svgwrite

from main.config.parse_layouts import read_from_file
from main.led_char_map import LedCharMap
from simulator.simulator import get_leds


def font_to_base64(font_path):
    with open(font_path, "rb") as font_file:
        encoded_font = base64.b64encode(font_file.read()).decode("utf-8")
    return encoded_font


def calculate_text_grid_positions(total_width, leds_per_meter, text_grid, vertical_stretch=1.0):
    # Calculate LED spacing in mm based on LEDs per meter
    led_spacing = 1000 / leds_per_meter  # Distance between LEDs in mm (1000 mm per meter)

    # Determine the number of rows and columns based on the text grid
    rows = len(text_grid)
    cols = len(text_grid[0])

    # Calculate effective width and height of the grid based on led_spacing and number of columns/rows
    grid_width = led_spacing * (cols - 1)
    grid_height = led_spacing * (rows - 1) * vertical_stretch  # Apply vertical stretch to height

    # Calculate the offset needed to center the grid within the total_width
    x_offset = (total_width - grid_width) / 2
    y_offset = (total_width - grid_height) / 2  # Assuming a square area for simplicity

    # Generate the positions for each LED in the text grid
    led_positions = []
    for row in range(rows):
        for col in range(cols):
            x = x_offset + col * led_spacing
            y = y_offset + row * led_spacing * vertical_stretch  # Apply vertical stretch to y position
            led_positions.append((x, y))

    return led_positions



def calculate_corner_led_positions(total_width, total_height, offset_from_edge):
    corner_leds = {
        "top_left": (offset_from_edge, offset_from_edge),
        "top_right": (total_width - offset_from_edge, offset_from_edge),
        "bottom_left": (offset_from_edge, total_height - offset_from_edge),
        "bottom_right": (total_width - offset_from_edge, total_height - offset_from_edge),
    }

    return corner_leds


def create_word_clock_svg(filename, total_width, total_height, line_width, corner_diameter ,text_grid, leds_per_meter, font_path, offset_from_edge,
                          font_size=24, padding=10):
    # Calculate the text grid and corner LED positions
    text_positions = calculate_text_grid_positions(total_width, leds_per_meter, text_grid, vertical_stretch = 1.1)
    corner_positions = calculate_corner_led_positions(total_width, total_height, offset_from_edge)

    # Convert the font to Base64 for embedding in the SVG
    base64_font = font_to_base64(font_path)

    # Define the SVG canvas dimensions
    dwg = svgwrite.Drawing(filename, profile='full', size=(total_width + 2 * padding, total_height + 2 * padding))

    # Add font style
    font_style = f"""
    @font-face {{
        font-family: 'CustomDINStencil';
        src: url("data:font/ttf;base64,{base64_font}") format("truetype");
    }}
    text {{
        font-family: 'CustomDINStencil';
        fill: white;
        font-size: {font_size}px;
        text-anchor: middle;
    }}
    """
    dwg.defs.add(dwg.style(content=font_style))

    # Add background
    dwg.add(dwg.rect(insert=(0, 0), size=(total_width + 2 * padding, total_height + 2 * padding), fill="black", stroke_width=line_width))

    # Add text grid LEDs based on calculated positions
    for index, (x, y) in enumerate(text_positions):
        row = index // len(text_grid[0])
        col = index % len(text_grid[0])
        char = text_grid[row][col]

        # Adjust x and y by padding for centering
        x_with_padding = x + padding
        y_with_padding = y + padding + font_size / 3  # Adjust Y for vertical centering

        dwg.add(dwg.text(char,
                         insert=(x_with_padding, y_with_padding),
                         fill="none",
                         fill_opacity=0,  # Ensures no fill is rendered
                         stroke="white",
                         stroke_width=line_width,  # Adjust the width of the text outline
                         font_size=font_size,
                         text_anchor="middle",
                         font_family="CustomDINStencil"))

    # Add corner LEDs based on calculated corner positions
    for name, (x, y) in corner_positions.items():
        # Example of a circle with a specified line width and no fill
        dwg.add(dwg.circle(center=(x + padding, y + padding), r=corner_diameter / 2,
                           fill="none", stroke="white", stroke_width=line_width))

    # Save the SVG file
    dwg.save()


# Define the text grid and parameters
text_grid = [
    ["E", "S", "K", "I", "S", "C", "H", "A", "F", "Ü", "F"],
    ["V", "I", "E", "R", "T", "U", "B", "F", "Z", "Ä", "Ä"],
    ["Z", "W", "Ä", "N", "Z", "G", "S", "I", "V", "O", "R"],
    ["A", "B", "O", "H", "A", "U", "B", "I", "E", "G", "E"],
    ["E", "I", "S", "Z", "W", "Ö", "I", "S", "D", "R", "Ü"],
    ["V", "I", "E", "R", "I", "F", "Ü", "F", "I", "Q", "T"],
    ["S", "Ä", "C", "H", "S", "I", "S", "I", "B", "N", "I"],
    ["A", "C", "H", "T", "I", "N", "Ü", "N", "I", "E", "L"],
    ["Z", "Ä", "N", "I", "E", "R", "B", "Ö", "U", "F", "I"],
    ["Z", "W", "Ö", "U", "F", "I", "N", "A", "U", "H", "R"]
]

# Parameters
total_width = 450  # Total width in mm
total_height = 450  # Total height in mm
leds_per_meter = 30  # LEDs per meter
offset_from_edge = 15  # Offset for corner LEDs in mm
corner_diameter = 3
line_width = 0.1
vertical_stretch = 1.05
font_path = r"C:\git\wordclock_pi\app\font\ruler-stencil\Ruler Stencil Light.ttf"

# Generate the SVG
create_word_clock_svg("word_clock.svg", total_width, total_height,line_width, corner_diameter, text_grid, leds_per_meter, font_path,
                      offset_from_edge)


config_path = r"C:\git\wordclock_pi\app\main\config\layouts.json"

layout_configs = read_from_file(config_path)
layout_config = layout_configs[0]
led_char_map = LedCharMap(layout_config=layout_config)

leds = get_leds(time=datetime.now(), led_char_map=led_char_map)

test = 1
# for led_image in led_images:
#     if led_image.led_number in leds:
#         img = led_image.on(r=255, g=0, b=0, image=img)
#         print(led_image)
#     else:
#         img = led_image.off(image=img)
#         print(led_image)

