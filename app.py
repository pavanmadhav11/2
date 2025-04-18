from flask import Flask, render_template, request
from converter import generate_flowchart_bokeh
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_flowchart', methods=['POST'])
def generate_flowchart():
    try:
        code = request.form['code']

        # Generate the flowchart and save it to static
        flowchart_file = generate_flowchart_bokeh(code)

        # Return the filename of the generated flowchart
        return render_template('index.html', flowchart=flowchart_file)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    # Bind to the port provided by Render (default is 5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
