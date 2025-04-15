import ast
import graphviz

class CodeToFlowchart(ast.NodeVisitor):
    def __init__(self):
        self.graph = graphviz.Digraph(format="png")
        self.node_count = 0
        self.prev_node = None
        self.error_detected = False

    def add_node(self, label):
        node_name = f"node{self.node_count}"
        self.graph.node(node_name, label, shape="box")
        if self.prev_node is not None:
            self.graph.edge(self.prev_node, node_name)
        self.prev_node = node_name
        self.node_count += 1
        return node_name

    def visit_FunctionDef(self, node):
        self.prev_node = self.add_node(f"Function: {node.name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = ", ".join([target.id for target in node.targets if isinstance(target, ast.Name)])
        value = ast.unparse(node.value) if hasattr(ast, "unparse") else ""
        self.add_node(f"{targets} = {value}")

    def visit_If(self, node):
        cond = ast.unparse(node.test) if hasattr(ast, "unparse") else ""
        if_node = self.add_node(f"IF {cond}?")
        prev = self.prev_node
        self.prev_node = if_node
        for stmt in node.body:
            self.visit(stmt)
        true_end = self.prev_node
        self.prev_node = if_node
        for stmt in node.orelse:
            self.visit(stmt)
        false_end = self.prev_node
        self.graph.edge(if_node, true_end, label="True")
        self.graph.edge(if_node, false_end, label="False")
        self.prev_node = false_end

    def visit_While(self, node):
        cond = ast.unparse(node.test) if hasattr(ast, "unparse") else ""
        loop_node = self.add_node(f"WHILE {cond}?")
        prev = self.prev_node
        self.prev_node = loop_node
        for stmt in node.body:
            self.visit(stmt)
        self.graph.edge(self.prev_node, loop_node, label="Loop Back")
        self.prev_node = loop_node

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
            self.graph.render("static/flowchart", format="png", cleanup=True)
            return True
        except SyntaxError as e:
            return False
