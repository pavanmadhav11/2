import ast
import matplotlib.pyplot as plt
from PIL import Image
import networkx as nx

class FlowchartGenerator(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.counter = 0
        self.last_node = None

    def _new_node(self, label):
        node_id = f"n{self.counter}"
        self.graph.add_node(node_id, label=label)
        if self.last_node is not None:
            self.graph.add_edge(self.last_node, node_id)
        self.last_node = node_id
        self.counter += 1
        return node_id

    def visit_FunctionDef(self, node):
        self.last_node = self._new_node(f"Function: {node.name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = ", ".join(ast.unparse(t) for t in node.targets)
        value = ast.unparse(node.value)
        self._new_node(f"{targets} = {value}")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            call_expr = ast.unparse(node.value)
            self._new_node(f"Call: {call_expr}")

    def visit_If(self, node):
        cond = ast.unparse(node.test)
        if_node = self._new_node(f"If {cond}?")
        prev = self.last_node
        for stmt in node.body:
            self.visit(stmt)
        self.graph.add_edge(if_node, self.last_node, label="True")
        self.last_node = if_node
        for stmt in node.orelse:
            self.visit(stmt)
        self.graph.add_edge(if_node, self.last_node, label="False")

    def visit_While(self, node):
        cond = ast.unparse(node.test)
        loop_node = self._new_node(f"While {cond}?")
        prev = self.last_node
        for stmt in node.body:
            self.visit(stmt)
        self.graph.add_edge(self.last_node, loop_node, label="Loop")
        self.last_node = loop_node

    def visit_Return(self, node):
        val = ast.unparse(node.value) if node.value else ""
        self._new_node(f"Return {val}")

    def generate(self, code):
        # Parse the code and visit each node using ast.NodeVisitor
        tree = ast.parse(code)
        self.visit(tree)

        # Create the flowchart visualization
        labels = nx.get_node_attributes(self.graph, 'label')
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, labels=labels, with_labels=True,
                node_size=3000, node_color="skyblue", font_size=8,
                font_weight='bold')
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title("Flowchart")
        plt.tight_layout()

        # Save the flowchart to a PNG file
        plt.savefig("flowchart.png")
        plt.close()

    def save(self, filename):
        # Save the flowchart to a file
        img = Image.open("flowchart.png")
        img.save(filename)

