import ast
from PIL import Image, ImageDraw, ImageFont

class FlowchartGenerator:
    def __init__(self, image_size=(800, 600), font_size=14):
        self.image = Image.new("RGB", image_size, color="white")
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()  # Use a default font
        self.x_offset = 50
        self.y_offset = 50
        self.node_width = 150
        self.node_height = 50
        self.spacing = 20

    def _draw_node(self, text, x, y):
        # Draw the rectangle for the node
        self.draw.rectangle([x, y, x + self.node_width, y + self.node_height], outline="black", width=2)
        # Add the text inside the node
        self.draw.text((x + 10, y + 10), text, fill="black", font=self.font)

    def _add_edge(self, start, end):
        # Draw an arrow from start to end (simple line for simplicity)
        self.draw.line([start[0] + self.node_width // 2, start[1] + self.node_height, end[0] + self.node_width // 2, end[1]], fill="black", width=2)
        self.draw.polygon([end[0] + self.node_width // 2 - 5, end[1], end[0] + self.node_width // 2 + 5, end[1], end[0] + self.node_width // 2, end[1] + 10], fill="black")

    def visit_FunctionDef(self, node):
        text = f"Function: {node.name}"
        x = self.x_offset
        y = self.y_offset
        self._draw_node(text, x, y)
        self.y_offset += self.node_height + self.spacing
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = ", ".join(ast.unparse(t) for t in node.targets)
        value = ast.unparse(node.value)
        text = f"{targets} = {value}"
        x = self.x_offset
        y = self.y_offset
        self._draw_node(text, x, y)
        self.y_offset += self.node_height + self.spacing

    def visit_If(self, node):
        cond = ast.unparse(node.test)
        text = f"If {cond}?"
        x = self.x_offset
        y = self.y_offset
        self._draw_node(text, x, y)
        start = (x, y)

        self.y_offset += self.node_height + self.spacing
        for stmt in node.body:
            self.visit(stmt)

        end = (x, self.y_offset)
        self._add_edge(start, end)

        self.y_offset += self.node_height + self.spacing
        for stmt in node.orelse:
            self.visit(stmt)

        self._add_edge(start, (x, self.y_offset))

    def visit_While(self, node):
        cond = ast.unparse(node.test)
        text = f"While {cond}?"
        x = self.x_offset
        y = self.y_offset
        self._draw_node(text, x, y)
        start = (x, y)

        self.y_offset += self.node_height + self.spacing
        for stmt in node.body:
            self.visit(stmt)

        self._add_edge((x, self.y_offset), start)

    def visit_Return(self, node):
        value = ast.unparse(node.value) if node.value else ""
        text = f"Return {value}"
        x = self.x_offset
        y = self.y_offset
        self._draw_node(text, x, y)
        self.y_offset += self.node_height + self.spacing

    def generate(self, code):
        tree = ast.parse(code)
        self.visit(tree)

    def save(self, filepath="flowchart.png"):
        self.image.save(filepath)

