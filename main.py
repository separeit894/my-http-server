from flask import Flask, request, render_template, send_file, redirect, url_for, abort
import os
from zipfile import ZipFile

app = Flask(__name__)

UPLOADS_DIR = "uploads"
ZIP_ARCHIVE_DIR = "zip_archive"
zip_filename = "files.zip"
os.makedirs(ZIP_ARCHIVE_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

VERSION = "0.0.4"

@app.route("/")
def index():
    data = os.listdir(UPLOADS_DIR)

    return render_template("index.html", data=data, version=f"version: {VERSION}", zipfile=zip_filename)

@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        path = os.path.join(UPLOADS_DIR, file.filename)
        file.save(path)

    return redirect("/")


@app.route("/get_file/<string:file>")
def get_file(file):
    path = os.path.join(UPLOADS_DIR, file)
    if os.path.exists(path):
        return send_file(path, as_attachment=False)

@app.route("/delete/<string:filename>")
def delete_file(filename):
    path = os.path.join(UPLOADS_DIR, filename)
    if os.path.exists(path):
        os.remove(path)

    return redirect("/")

@app.route("/create-zip-archive", methods=["POST"])
def create_zip_archive():
    zip_path = os.path.join(ZIP_ARCHIVE_DIR, zip_filename)

    if request.method == "POST":    
        result = request.get_json()

        if os.path.exists(zip_path):
            print(f"[ DELETE ] File exists: {zip_path}... Delete file")
            os.remove(zip_path)
        
        with ZipFile(zip_path, "w") as myzip:
            for i in result:
                src_path = os.path.join(UPLOADS_DIR, i)
                if os.path.exists(src_path):
                    myzip.write(src_path)
                else:
                    print(f"File not founded : {src_path}")
            myzip.close()

        return send_file(zip_path, as_attachment=False, download_name=zip_filename)
    else:
        return render_template("page_not_found.html")

@app.route("/get-zip-archive/<string:zipfile>", methods=['GET', 'POST'])
def get_zip_archive(zipfile):
    import time
    time.sleep(3)
    return send_file(os.path.join(ZIP_ARCHIVE_DIR, zipfile), as_attachment=False, download_name=zip_filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")