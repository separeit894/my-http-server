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
from core import (
    CONFIG_JSON,
    create_config_json,
    read_config_json,
    write_data_to_config_json
)

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
start_create_zip = False
created_zip = False

# Make dirs if not exists
os.makedirs(ZIP_ARCHIVE_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

VERSION = "0.1.1"

DATA_CONFIG = read_config_json()

@app.route("/")
def index():
    data = os.listdir(UPLOADS_DIR)

    if os.path.exists(FULL_PATH_ZIPFILE):
        os.remove(FULL_PATH_ZIPFILE)

    return render_template("index.html", data=data, version=f"version: {VERSION}", zipfile=ZIP_FILENAME, dict=DATA_CONFIG["Security"])


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

    security_list = DATA_CONFIG["Security"]

    if filename in security_list:
        print("[ NOT REMOVE FILE FROM SECURITY LIST IN CONFIG, THAT`S NOT DELETE FILE]")
        return redirect("/")
        
    else:
        if os.path.exists(path):
            os.remove(path)
        print("[ DELETE THIS FILE, THAT'S NOT EXISTS IN SECURITY LIST ]")

    return redirect("/")


@app.route("/create-zip-archive", methods=["POST"])
def create_zip_archive():
    global start_create_zip, created_zip

    if request.method == "POST":    
        result = request.get_json()

        if os.path.exists(FULL_PATH_ZIPFILE):
            print(f"[ DELETE ] File exists: {FULL_PATH_ZIPFILE}... Delete file")
            os.remove(FULL_PATH_ZIPFILE)

        start_create_zip = True
        print(f"[ START CREATE ZIP ] : {start_create_zip}")
        created_zip = False

        with ZipFile(FULL_PATH_ZIPFILE, "w") as myzip:
            print(result)
            for i in result:
                src_path = os.path.join(UPLOADS_DIR, i)
                if os.path.exists(src_path):
                    myzip.write(src_path, arcname=i.split(os.sep)[-1])
                else:
                    print(f"File not founded : {src_path}")

            myzip.close()
            created_zip = True
            print(f"[ CREATE ZIP FILE ] : created_zip : {created_zip}")

        return send_file(FULL_PATH_ZIPFILE, as_attachment=True, download_name=ZIP_FILENAME)
    else:
        return render_template("page_not_found.html")


@app.route("/get-zip-archive", methods=['GET', 'POST'])
def get_zip_archive():
    global start_create_zip

    @after_this_request
    def delete_zip_file(response):
        if os.path.exists(FULL_PATH_ZIPFILE):
            print(f"[ DELETE ZIPFILE IF EXISTS ] : {FULL_PATH_ZIPFILE}")
            os.remove(FULL_PATH_ZIPFILE)

        return response
    print(f"NOW : {start_create_zip}")
    if start_create_zip:
        while not created_zip:
            time.sleep(2)
            print(f"[ VARIABLE CREATED_ZIP ] : {created_zip}")
            if created_zip:
                break

        start_create_zip = False

        return send_file(FULL_PATH_ZIPFILE, as_attachment=False, download_name=ZIP_FILENAME)
    else:
        return redirect("/")

@app.route("/security-file", methods=["POST"])
def security_file():
    if request.method == "POST":
        result = request.get_json()
        if create_config_json():
            for item in result:
                if item in DATA_CONFIG["Security"]:
                    print(f"[ ITEM EXISTS IN LIST, THAT`S NOT APPEND IN LIST ] : {item}")
                else:
                    print(f"[ ITEM APPEND IN LIST ] : {item}")
                    DATA_CONFIG["Security"].append(item)

            if DATA_CONFIG != read_config_json():
                write_data_to_config_json(DATA_CONFIG)
            else:
                print("[ NOT WRITE DATA, THAT`S NOT NEW DATA]")

        return redirect("/")

@app.route("/delete-security-file", methods=["POST"])
def delete_security_file():
    if request.method == "POST":
        result = request.get_json()
        if create_config_json():
            security_file = DATA_CONFIG["Security"]
            for item in result:
                if item in security_file:
                    security_file.remove(item)
                    print(f"[ REMOVE ITEM IN SECURITY FILE LIST : {item} ]")
                        
            if DATA_CONFIG != read_config_json():
                write_data_to_config_json(DATA_CONFIG)
            else:
                print("[ NOT WRITE DATA, THAT`S NOT NEW DATA]")

            return redirect(url_for("index"))
    

@app.errorhandler(404)
def error_page(error):
    return render_template("page_not_found.html")

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)