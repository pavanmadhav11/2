import ast
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, LabelSet

class CodeToFlowchart(ast.NodeVisitor):
    def __init__(self):
        self.node_count = 0
        self.nodes = []
        self.edges = []

    def add_node(self, label):
        node_name = f"node{self.node_count}"
        self.nodes.append({'id': node_name, 'label': label, 'x': 0, 'y': self.node_count * -100})
        if self.node_count > 0:
            self.edges.append((f"node{self.node_count - 1}", node_name))  # Connect to previous node
        self.node_count += 1
        return node_name

    def visit_FunctionDef(self, node):
        self.add_node(f"Function: {node.name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = ", ".join([target.id for target in node.targets if isinstance(target, ast.Name)])
        value = ast.unparse(node.value) if hasattr(ast, "unparse") else ""
        self.add_node(f"{targets} = {value}")

    def visit_If(self, node):
        cond = ast.unparse(node.test) if hasattr(ast, "unparse") else ""
        if_node = self.add_node(f"IF {cond}?")
        self.generic_visit(node)

    def visit_While(self, node):
        cond = ast.unparse(node.test) if hasattr(ast, "unparse") else ""
        loop_node = self.add_node(f"WHILE {cond}?")
        self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            func_name = ast.unparse(node.value.func) if hasattr(ast, "unparse") else ""
            self.add_node(f"Call: {func_name}()")

    def visit_Return(self, node):
        value = ast.unparse(node.value) if hasattr(ast, "unparse") else ""
        self.add_node(f"Return {value}")

    def generate_flowchart(self, code):
        try:
            tree = ast.parse(code)
            self.visit(tree)

            # Prepare Bokeh plot
            p = figure(title="Code Flowchart", tools="", x_range=(-1, 2), y_range=(-self.node_count, 1))
            p.xgrid.visible = False
            p.ygrid.visible = False

            # Plot nodes as text
            source = ColumnDataSource(data=dict(
                x=[node['x'] for node in self.nodes],
                y=[node['y'] for node in self.nodes],
                label=[node['label'] for node in self.nodes]
            ))
            labels = LabelSet(x='x', y='y', text='label', source=source, text_align='center')
            p.add_layout(labels)

            # Plot edges (connections between nodes)
            for edge in self.edges:
                p.line([self.nodes[int(edge[0][4:])]['x'], self.nodes[int(edge[1][4:])]['x']],
                       [self.nodes[int(edge[0][4:])]['y'], self.nodes[int(edge[1][4:])]['y']],
                       line_width=2, color="gray")

            # Save output to HTML file
            output_file("static/flowchart.html")
            save(p)

            return "flowchart.html"
        except SyntaxError as e:
            return False
