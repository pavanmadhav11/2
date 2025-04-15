import ast
import networkx as nx
import matplotlib.pyplot as plt

class FlowchartGenerator(ast.NodeVisitor):
    def __init__(self):
        self.graph = nx.DiGraph()
        self.counter = 0
        self.last_node = None

    def _new_node(self, label, node_type="box"):
        node_id = f"n{self.counter}"
        self.graph.add_node(node_id, label=label, node_type=node_type)
        if self.last_node is not None:
            self.graph.add_edge(self.last_node, node_id)
        self.last_node = node_id
        self.counter += 1
        return node_id

    def visit_FunctionDef(self, node):
        self.last_node = self._new_node(f"Function: {node.name}", node_type="ellipse")
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = ", ".join(ast.unparse(t) for t in node.targets)
        value = ast.unparse(node.value)
        self._new_node(f"{targets} = {value}", node_type="box")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            call_expr = ast.unparse(node.value)
            self._new_node(f"Call: {call_expr}", node_type="box")

    def visit_If(self, node):
        cond = ast.unparse(node.test)
        if_node = self._new_node(f"If {cond}?", node_type="diamond")
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
        loop_node = self._new_node(f"While {cond}?", node_type="diamond")
        prev = self.last_node
        for stmt in node.body:
            self.visit(stmt)
        self.graph.add_edge(self.last_node, loop_node, label="Loop")
        self.last_node = loop_node

    def visit_Return(self, node):
        val = ast.unparse(node.value) if node.value else ""
        self._new_node(f"Return {val}", node_type="box")

    def generate(self, code):
        tree = ast.parse(code)
        self.visit(tree)

    def save(self, filepath="static/flowchart.png"):
        labels = nx.get_node_attributes(self.graph, 'label')
        node_types = nx.get_node_attributes(self.graph, 'node_type')

        # Using spring layout with a seed for better stability of the layout
        pos = nx.spring_layout(self.graph, seed=42, k=0.6, iterations=30)

        # Draw nodes with different shapes depending on node type
        for node, node_type in node_types.items():
            shape = "s" if node_type == "box" else "o" if node_type == "ellipse" else "^"
            nx.draw_networkx_nodes(self.graph, pos, [node], node_size=3000, node_color="skyblue", node_shape=shape)
        
        # Draw edges with specific attributes
        nx.draw_networkx_edges(self.graph, pos, width=2, alpha=0.6, edge_color="gray")

        # Draw labels for nodes and edges
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=10, font_weight='bold', font_color="black")
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8, font_color="black")

        # Set the title and remove axis
        plt.title("Flowchart Representation of Python Code", fontsize=14)
        plt.axis("off")

        # Save the figure as a PNG file
        plt.tight_layout()
        plt.savefig(filepath)
        plt.clf()
