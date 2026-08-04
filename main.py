from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not os.path.exists("uploads"):
            os.mkdir("uploads")
        file.save(f"uploads/{file.filename}")
        return render_template("index.html")

@app.route("/list")
def list_files():
    data = os.listdir("uploads/")
    return render_template("list.html", data=data)


@app.route("/uploads/<string:file>")
def get_file(file):
    if os.path.exists(f"uploads/{file}"):
        return send_file(f"uploads/{file}", as_attachment=False)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")