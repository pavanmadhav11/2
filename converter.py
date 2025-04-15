import ast
from pyflowchart import Flowchart

class CodeToFlowchart:
    def __init__(self):
        self.error_detected = False

    def generate_flowchart(self, code):
        try:
            # Parse the code and generate flowchart
            fc = Flowchart.from_code(code)
            flowchart_text = fc.flowchart()
            
            # Return the flowchart text to be rendered by flowchart.js
            return {
                'flowchart_text': flowchart_text,
                'nodes': self._count_nodes(flowchart_text)
            }
        except SyntaxError as e:
            self.error_detected = True
            return False

    def _count_nodes(self, flowchart_text):
        # Helper method to count nodes for display purposes
        return len([line for line in flowchart_text.split('\n') 
                  if line.strip() and '=>' in line])
