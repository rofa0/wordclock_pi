import base64
from datetime import datetime
from io import StringIO

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


def create_word_clock_svg(filename, total_width, total_height, line_width, corner_diameter, led_char_map, leds_per_meter, font_path, offset_from_edge,
                          font_size=24, padding=10, active_leds=None, animation=True):
    # Calculate the text grid and corner LED positions
    text_positions = calculate_text_grid_positions(total_width, leds_per_meter, led_char_map.letter_matrix, vertical_stretch=1.1)
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
        font-size: {font_size}px;
        text-anchor: middle;
    }}
    """
    dwg.defs.add(dwg.style(content=font_style))

    # Add background
    dwg.add(dwg.rect(insert=(0, 0), size=(total_width + 2 * padding, total_height + 2 * padding), fill="black"))



    # Add text grid LEDs based on calculated positions
    for row in range(len(led_char_map.letter_matrix)):
        for col in range(len(led_char_map.letter_matrix[0])):
            char = led_char_map.letter_matrix[row][col]
            led_number = led_char_map.led_number_matrix[row][col]

            # Determine if this LED should be highlighted based on active_leds
            text_fill = "red" if active_leds and led_number in active_leds else "grey"

            # Calculate position
            x_with_padding = text_positions[row * len(led_char_map.letter_matrix[0]) + col][0] + padding
            y_with_padding = text_positions[row * len(led_char_map.letter_matrix[0]) + col][1] + padding + font_size / 3

            dwg.add(dwg.text(char,
                             insert=(x_with_padding, y_with_padding),
                             fill=text_fill,
                             stroke=text_fill,  # Use the same color for stroke
                             stroke_width=line_width,  # Adjust the width of the text outline
                             font_size=font_size,
                             text_anchor="middle",
                             font_family="CustomDINStencil"))

    # Map minute values to specific corner positions

    corner_pos_to_minute = {
        "top_left": 1,  # 1 minute corresponds to top-left corner
        "top_right": 2,  # 2 minutes corresponds to top-right corner
        "bottom_left": 3,  # 3 minutes corresponds to bottom-left corner
        "bottom_right": 4  # 4 minutes corresponds to bottom-right corner
    }


    # Add corner LEDs based on calculated corner positions
    for corner_name, (x, y) in corner_positions.items():
        # Check if this corner LED should be highlighted
        corner_number = corner_pos_to_minute.get(corner_name)
        corner_led_number = led_char_map.corners.get(corner_number)

        corner_fill = "red" if active_leds and corner_led_number in active_leds else "grey"

        dwg.add(dwg.circle(center=(x + padding, y + padding), r=corner_diameter / 2,
                           fill=corner_fill, stroke=corner_fill, stroke_width=line_width))


    # If animation is enabled, embed JavaScript directly into the SVG
    if animation:
        script = """
        function updateClock() {
            const now = new Date();
            const hour = now.getHours() % 12 || 12;
            const minute = now.getMinutes();
            const minuteRounded = Math.floor(minute / 5) * 5;
            const extraMinutes = minute % 5;

            // Reset all LEDs to inactive (grey)
            document.querySelectorAll('.text-led').forEach(el => el.setAttribute("fill", "grey"));
            document.querySelectorAll('.corner-led').forEach(el => el.setAttribute("fill", "grey"));

            // Activate LEDs for the hour and minute
            document.querySelectorAll(`.hour-${hour}`).forEach(el => el.setAttribute("fill", "red"));
            if (minuteRounded > 0) {
                document.querySelectorAll(`.minute-${minuteRounded}`).forEach(el => el.setAttribute("fill", "red"));
            }

            // Highlight the corner LED for additional minutes
            if (extraMinutes > 0) {
                document.getElementById(`corner-led-${extraMinutes}`).setAttribute("fill", "red");
            }
        }

        // Update the clock every second
        setInterval(updateClock, 1000);
        updateClock();  // Initial call
        """
        # Embed the script in the SVG
        dwg.defs.add(dwg.script(content=script, type="text/ecmascript"))

    # Save the SVG file
    return dwg



def create_svg_main(time: datetime):
    # Parameters
    total_width = 450  # Total width in mm
    total_height = 450  # Total height in mm
    leds_per_meter = 30  # LEDs per meter
    offset_from_edge = 15  # Offset for corner LEDs in mm
    corner_diameter = 3
    line_width = 0.1
    vertical_stretch = 1.05
    font_path = r"C:\git\wordclock_pi\app\font\ruler-stencil\Ruler Stencil Light.ttf"


    config_path = r"C:\git\wordclock_pi\app\main\config\layouts.json"

    layout_configs = read_from_file(config_path)
    layout_config = layout_configs[0]

    led_char_map = LedCharMap(layout_config=layout_config)
    active_leds = get_leds(time=time, led_char_map=led_char_map)

    # Usage Example
    svg = create_word_clock_svg("word_clock.svg", total_width, total_height, line_width, corner_diameter, led_char_map, leds_per_meter, font_path,
                          offset_from_edge, active_leds=active_leds)

    # Write to an in-memory buffer
    svg_buffer = StringIO()
    svg.write(svg_buffer)
    svg_buffer.seek(0)

    return svg_buffer.getvalue()



if __name__ == "__main__":

    # Parameters
    total_width = 450  # Total width in mm
    total_height = 450  # Total height in mm
    leds_per_meter = 30  # LEDs per meter
    offset_from_edge = 15  # Offset for corner LEDs in mm
    corner_diameter = 3
    line_width = 0.1
    vertical_stretch = 1.05
    font_path = r"C:\git\wordclock_pi\app\font\ruler-stencil\Ruler Stencil Light.ttf"

    config_path = r"C:\git\wordclock_pi\app\main\config\layouts.json"

    layout_configs = read_from_file(config_path)
    layout_config = layout_configs[0]

    led_char_map = LedCharMap(layout_config=layout_config)
    active_leds = get_leds(time=datetime.now(), led_char_map=led_char_map)

    # Usage Example
    svg = create_word_clock_svg("word_clock_test.svg", total_width, total_height, line_width, corner_diameter,
                                led_char_map, leds_per_meter, font_path,
                                offset_from_edge, active_leds=active_leds)

    svg.save()