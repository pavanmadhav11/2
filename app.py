from flask import Flask, render_template, request
from convertor import FlowchartGenerator
import os
import traceback

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_url = None
    error = None

    if request.method == "POST":
        try:
            code = request.form.get("code", "")
            if not code.strip():
                error = "Please enter some code!"
                return render_template("index.html", chart_url=None, error=error)

            # Initialize the flowchart generator
            fc = FlowchartGenerator()
            flowchart_image_path = fc.generate(code)

            if flowchart_image_path:
                chart_url = f"/static/{flowchart_image_path}"
            else:
                error = "Syntax Error in your code. Please fix it."

        except Exception as e:
            traceback.print_exc()  # Print full traceback to logs
            error = f"Something went wrong: {str(e)}"

    return render_template("index.html", chart_url=chart_url, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(debug=False, host="0.0.0.0", port=port)
