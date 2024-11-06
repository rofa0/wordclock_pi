import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# Define parameters
total_width = 450
total_height = 450
font_size = 16
corner_diameter = 10
padding = 20

# Word clock layout (replace with actual layout if different)
text_grid = [
    ["E", "S", "K", "I", "S", "C", "H", "A", "F", "Ü", "F"],
    ["V", "I", "E", "R", "T", "U", "B", "F", "Z", "Ä", "Ä"],
    # ... Add remaining rows as needed
]

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(6, 6))
ax.axis('off')  # Turn off axes

# Initial placement of letters and corner dots
text_objects = []
for row, line in enumerate(text_grid):
    for col, char in enumerate(line):
        # Calculate position for each character
        x = padding + col * (total_width / len(line))
        y = total_height - (padding + row * (total_height / len(text_grid)))
        text_obj = ax.text(x, y, char, ha='center', va='center', fontsize=font_size, color='grey')
        text_objects.append((text_obj, row, col))  # Store text object with position info

# Define corner positions (in mm or any consistent units)
corner_positions = {
    1: (padding, padding),                      # Top-left corner for minute 1
    2: (total_width - padding, padding),        # Top-right corner for minute 2
    3: (padding, total_height - padding),       # Bottom-left corner for minute 3
    4: (total_width - padding, total_height - padding)  # Bottom-right corner for minute 4
}
corner_circles = {}
for minute, (x, y) in corner_positions.items():
    circle = plt.Circle((x, y), corner_diameter / 2, color='grey')
    ax.add_patch(circle)
    corner_circles[minute] = circle

# Update function for each frame
def update_frame(frame):
    current_time = datetime.now()
    hour = current_time.hour % 12 or 12  # Convert to 12-hour format
    minute = current_time.minute
    minute_rounded = (minute // 5) * 5
    extra_minutes = minute % 5

    # Reset all text and corner colors
    for text_obj, _, _ in text_objects:
        text_obj.set_color("grey")
    for circle in corner_circles.values():
        circle.set_color("grey")

    # Highlight hour and rounded minute in red
    for text_obj, row, col in text_objects:
        char = text_grid[row][col]
        # Logic for activating specific text (replace with actual logic)
        # Example:
        # if (char is part of `hour`) or (char is part of `minute_rounded`)
        #     text_obj.set_color("red")

    # Activate the corner LED based on extra minutes (1 to 4)
    if extra_minutes in corner_circles:
        corner_circles[extra_minutes].set_color("red")

    return text_objects + list(corner_circles.values())

# Animate using FuncAnimation
ani = FuncAnimation(fig, update_frame, interval=1000)  # Update every 1 second
plt.show()
