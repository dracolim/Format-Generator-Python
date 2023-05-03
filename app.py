from flask import Flask, jsonify, render_template, request, redirect, url_for , send_file, send_from_directory
import os
import json
import base64
from io import BytesIO
from flask_cors import CORS

# from flask_login import login_required, current_user
app = Flask(__name__)

# CORS(app)
app = Flask(__name__)
app.app_context().push()
app.secret_key = b'a secret key'

CORS(app)


# IMPORT
@app.route('/import', methods=['POST'])
def view():
    file = request.files['file']
    file.save(file.filename)

    filename = file.filename 

    with open(filename) as f: 
        for i , each_line in enumerate(f):
            

    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)