from flask import Flask, render_template, jsonify, Response, redirect
from datetime import datetime
import svgwrite
from io import BytesIO

from plate.generate2 import create_svg_main

app = Flask(__name__)


@app.route('/api/')
def api_svg():
    """API endpoint that generates and returns the SVG of the word clock based on the current time."""

    # Generate SVG in memory
    svg_data = create_svg_main(time=datetime.now())


    # Return SVG content as a response
    return Response(svg_data, mimetype='image/svg+xml')

@app.route('/')
def render_clock():
    """Renders the main page that displays the live word clock."""
    return redirect("api_svg")


if __name__ == '__main__':
    app.run(debug=True)