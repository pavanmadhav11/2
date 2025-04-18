import ast
import networkx as nx
from bokeh.io import export_png
from bokeh.plotting import figure, from_networkx
from bokeh.models import HoverTool
import os

# Make sure the static folder exists
STATIC_FOLDER = os.path.join(os.getcwd(), 'static')

if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

def build_ast_graph(code):
    """Builds a networkx graph from the Python code's AST"""
    tree = ast.parse(code)
    graph = nx.DiGraph()
    counter = {"id": 0}

    def get_id():
        counter["id"] += 1
        return f"node{counter['id']}"

    def visit(node, parent_id=None):
        node_id = get_id()
        label = type(node).__name__
        graph.add_node(node_id, label=label)

        if parent_id:
            graph.add_edge(parent_id, node_id)

        for child in ast.iter_child_nodes(node):
            visit(child, node_id)

    visit(tree)
    return graph

def render_bokeh_graph(graph, filename):
    """Generates a Bokeh plot from the networkx graph and saves it as a PNG"""
    plot = figure(title="Python Flowchart", x_range=(-1.5, 1.5), y_range=(-1.5, 1.5),
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom')

    plot.axis.visible = False
    plot.grid.visible = False

    layout = nx.spring_layout(graph, seed=42)
    bokeh_graph = from_networkx(graph, layout)

    # Add hover tool
    hover = HoverTool(tooltips=[("Node", "@label")])
    plot.add_tools(hover)

    bokeh_graph.node_renderer.data_source.data['label'] = [graph.nodes[n]['label'] for n in graph.nodes]
    bokeh_graph.node_renderer.glyph.size = 20
    bokeh_graph.node_renderer.glyph.fill_color = "skyblue"

    plot.renderers.append(bokeh_graph)

    # Save the plot as a PNG file in the static folder
    output_png_path = os.path.join(STATIC_FOLDER, filename)
    export_png(plot, filename=output_png_path)

    return filename  # Return the relative path for the image file

def generate_flowchart_png(code):
    """Converts Python code to a flowchart and saves it as a PNG in the static folder"""
    graph = build_ast_graph(code)
    flowchart_filename = "flowchart.png"
    flowchart_file = render_bokeh_graph(graph, flowchart_filename)
    return flowchart_file
