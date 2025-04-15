from flask import Flask, render_template, request
from converter import CodeToFlowchart
import os
import traceback

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    flowchart_data = None
    error = None

    if request.method == "POST":
        try:
            code = request.form.get("code", "")
            if not code.strip():
                error = "Please enter some code!"
                return render_template("index.html", flowchart_data=None, error=error)

            converter = CodeToFlowchart()
            flowchart_data = converter.generate_flowchart(code)

            if not flowchart_data:
                error = "Syntax Error in your code. Please fix it."

        except Exception as e:
            traceback.print_exc()
            error = f"Something went wrong: {str(e)}"

    return render_template("index.html", flowchart_data=flowchart_data, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
