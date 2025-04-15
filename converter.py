import ast
from pyflowchart import Flowchart

class CodeToFlowchart:
    def __init__(self):
        self.error_detected = False

    def generate_flowchart(self, code):
        try:
            # Add wrapper function if needed
            wrapped_code = self._wrap_code_if_needed(code)
            
            # Generate the flowchart
            fc = Flowchart.from_code(wrapped_code)
            flowchart_text = fc.flowchart()
            
            # Clean and simplify the flowchart text
            cleaned_text = self._clean_flowchart_text(flowchart_text)
            
            return {
                'flowchart_text': cleaned_text,
                'nodes': self._count_nodes(flowchart_text)
            }
        except Exception as e:
            print(f"Error generating flowchart: {str(e)}")
            return False

    def _wrap_code_if_needed(self, code):
        """Wrap simple statements in a function if needed."""
        if not code.strip().startswith(('def ', 'class ', '@')):
            # Indent all lines and add function wrapper
            indented_code = '\n'.join(f'    {line}' if line.strip() else line 
                                    for line in code.split('\n'))
            return f"def wrapper():\n{indented_code}"
        return code

    def _clean_flowchart_text(self, text):
        """Clean up the flowchart text for better display."""
        text = text.replace('`', '\\`').replace('$', '\\$')
        if "wrapper()" in text:
            text = text.replace("st=>start: wrapper()", "st=>start: Start")
            text = text.replace("e=>end: wrapper()", "e=>end: End")
        return text

    def _count_nodes(self, flowchart_text):
        """Count the number of nodes in the flowchart."""
        return len([line for line in flowchart_text.split('\n') 
                  if line.strip() and '=>' in line])
