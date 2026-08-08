from flask import (
    Flask, 
    request, 
    render_template, 
    send_file, 
    redirect, 
    url_for, 
    abort, 
    after_this_request,
    jsonify
)

from zipfile import ZipFile

import os
import time


app = Flask(__name__)

# Settings
HOST="0.0.0.0"
PORT="5000"

# Dirs
UPLOADS_DIR = "uploads"
ZIP_ARCHIVE_DIR = "zip_archive"

# Files
ZIP_FILENAME = "files.zip"

# FULL PATH 
FULL_PATH_ZIPFILE = os.path.join(ZIP_ARCHIVE_DIR, ZIP_FILENAME)

# if create zip, return file to download
create_zip = False

# Make dirs if not exists
os.makedirs(ZIP_ARCHIVE_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)


VERSION = "0.0.6"


@app.route("/")
def index():
    data = os.listdir(UPLOADS_DIR)

    if os.path.exists(FULL_PATH_ZIPFILE):
        os.remove(FULL_PATH_ZIPFILE)

    return render_template("index.html", data=data, version=f"version: {VERSION}", zipfile=ZIP_FILENAME)


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
    global create_zip

    if request.method == "POST":    
        result = request.get_json()

        if os.path.exists(FULL_PATH_ZIPFILE):
            print(f"[ DELETE ] File exists: {FULL_PATH_ZIPFILE}... Delete file")
            os.remove(FULL_PATH_ZIPFILE)

        create_zip = False

        with ZipFile(FULL_PATH_ZIPFILE, "w") as myzip:
            print(result)
            for i in result:
                src_path = os.path.join(UPLOADS_DIR, i)
                if os.path.exists(src_path):
                    myzip.write(src_path, arcname=i.split(os.sep)[-1])
                else:
                    print(f"File not founded : {src_path}")

            myzip.close()
            create_zip = True
            print(f"[ CREATE ZIP FILE ] : create_zip : {create_zip}")

        return send_file(FULL_PATH_ZIPFILE, as_attachment=True, download_name=ZIP_FILENAME)
    else:
        return render_template("page_not_found.html")


@app.route("/get-zip-archive", methods=['GET', 'POST'])
def get_zip_archive():
    while not create_zip:
        time.sleep(2)
        print(f"[ VARIABLE CREATE_ZIP ] : {create_zip}")
        if create_zip:
            break


    @after_this_request
    def delete_zip_file(response):
        if os.path.exists(FULL_PATH_ZIPFILE):
            print(f"[ DELETE ZIPFILE IF EXISTS ] : {FULL_PATH_ZIPFILE}")
            os.remove(FULL_PATH_ZIPFILE)

        return response

    try:
        return send_file(FULL_PATH_ZIPFILE, as_attachment=False, download_name=ZIP_FILENAME)
    except FileNotFoundError:
        return jsonify({"status": "error"})

@app.errorhandler(404)
def error_page(error):
    return render_template("page_not_found.html")

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)