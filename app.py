from flask import Flask, render_template, request
from converter import CodeToFlowchart
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_url = None
    error = None
    if request.method == "POST":
        code = request.form["code"]
        converter = CodeToFlowchart()
        flowchart = converter.generate_flowchart(code)
        if flowchart:
            filename = "static/flowchart"
            flowchart.render(filename, format="png", cleanup=True)
            chart_url = f"{filename}.png"
        else:
            error = "Syntax Error in your code. Please fix it."
    return render_template("index.html", chart_url=chart_url, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(debug=False, host="0.0.0.0", port=port)
