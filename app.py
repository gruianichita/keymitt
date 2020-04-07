import datetime
import logging
import os
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo

logging.basicConfig(level=logging.INFO)
load_dotenv(verbose=True)
app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
mongo = PyMongo(app)


@app.route('/application/', methods=['GET'])
def application_download():
    version = request.args.get('version')
    if not version:
        return jsonify({'err_msg': 'Missed version argument'}), 400
    document = mongo.db.application.find_one({'version': {'$gt': float(version)}}, sort=[('version', -1)])
    if document:
        file_name = document.get('filename')
        return send_file(BytesIO(document.get('filebody')), attachment_filename=file_name, as_attachment=True)
    else:
        return jsonify({'err_msg': 'No updates'}), 400


@app.route('/application/', methods=['POST'])
def application_upload():
    version = request.form.get('version')
    files = request.files
    if files and version:
        file = files['file']
        now = datetime.datetime.now()
        app_data = {
            'updated_at': now,
            'filename': file.filename,
            'filebody': file.read()
        }
        mongo.db.application.update_one({'version': float(version)}, {'$set': app_data}, True)
        return jsonify({'err_msg': ''}), 201
    else:
        return jsonify({'err_msg': 'File or version is empty'}), 400



if __name__ == '__main__':
    app.run()
