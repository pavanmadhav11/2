# app.py
from flask import Flask, render_template, request, send_file
from converter import FlowchartGenerator
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    flowchart_path = None
    if request.method == "POST":
        code = request.form["code"]
        generator = FlowchartGenerator()
        output_path = "static/flowchart.png"
        generator.generate(code, output_path=output_path)
        flowchart_path = output_path if os.path.exists(output_path) else None
    return render_template("index.html", image=flowchart_path)

@app.route("/download")
def download():
    return send_file("static/flowchart.png", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
