from bokeh.plotting import figure, output_file, save
from bokeh.models import Label
import os

def generate_flowchart_bokeh(code):
    try:
        # Output the flowchart as a static HTML file
        output_path = 'static/flowchart.html'
        output_file(output_path)

        # Create a Bokeh figure
        p = figure(title="Flowchart of Python Code", x_range=(0, 10), y_range=(0, 10))

        # Example flowchart with Bokeh (You can add more logic to visualize actual Python code structure)
        p.circle(x=[1, 3, 5], y=[8, 5, 2], size=20, color="blue", alpha=0.6)

        # Add labels
        p.add_layout(Label(x=1, y=8, text="Start"))
        p.add_layout(Label(x=3, y=5, text="Code Block"))
        p.add_layout(Label(x=5, y=2, text="End"))

        # Save the plot as HTML (you can use PNG via export_png if required)
        save(p)

        return 'flowchart.html'

    except Exception as e:
        raise e
