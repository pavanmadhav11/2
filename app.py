from flask import Flask, render_template, request, jsonify, url_for
from converter import generate_flowchart_png

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML template

@app.route('/generate_flowchart', methods=['POST'])
def generate_flowchart():
    try:
        # Extract Python code from the request JSON body
        data = request.get_json()
        code = data['code']

        # Generate the flowchart PNG and save it in the static folder
        flowchart_file = generate_flowchart_png(code)

        # Generate the URL for the flowchart image in the static folder
        flowchart_url = url_for('static', filename=flowchart_file)

        # Return the flowchart URL as response
        return jsonify({"flowchart_url": flowchart_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
