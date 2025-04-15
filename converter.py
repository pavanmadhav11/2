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
            
            # Clean the flowchart text for JavaScript
            cleaned_text = flowchart_text.replace('`', '\\`').replace('$', '\\$')
            
            return {
                'flowchart_text': cleaned_text,
                'nodes': self._count_nodes(flowchart_text)
            }
        except SyntaxError as e:
            self.error_detected = True
            return False
        except Exception as e:
            print(f"Error generating flowchart: {str(e)}")
            return False

    def _count_nodes(self, flowchart_text):
        return len([line for line in flowchart_text.split('\n') 
                  if line.strip() and '=>' in line])
