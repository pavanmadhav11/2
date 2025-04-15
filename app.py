from flask import Flask, render_template, request, send_file
from convertor import FlowchartGenerator
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form["code"]
        try:
            generator = FlowchartGenerator()
            generator.generate(code)

            # Save flowchart
            output_path = "static/flowchart.png"
            generator.save(output_path)

            return render_template("index.html", image="flowchart.png", code=code)
        except Exception as e:
            return render_template("index.html", error=str(e), code=code)
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_file(os.path.join("static", filename))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
