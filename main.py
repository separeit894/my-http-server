from flask import Flask, request, render_template, send_file, redirect, url_for
import os

app = Flask(__name__)

UPLOADS_DIR = "uploads"

@app.route("/")
def index():
    data = os.listdir(UPLOADS_DIR)
    return render_template("index.html", data=data)

@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not os.path.exists(UPLOADS_DIR):
            os.mkdir(UPLOADS_DIR)
        else:
            path = UPLOADS_DIR + "/" + file.filename
            file.save(path)

    return redirect("/")


@app.route("/get_file/<string:file>")
def get_file(file):
    path = UPLOADS_DIR + "/" + file
    if os.path.exists(path):
        return send_file(path, as_attachment=False)

@app.route("/delete/<string:filename>")
def delete_file(filename):
    path = UPLOADS_DIR + "/" + filename
    if os.path.exists(path):
        os.remove(path)
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")