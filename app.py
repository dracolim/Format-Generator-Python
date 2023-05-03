from flask import Flask, jsonify, render_template, request, redirect, url_for , send_file, send_from_directory
import os
from os import environ
import json
import base64
from io import BytesIO
from flask_cors import CORS
from werkzeug.utils import secure_filename

# from flask_login import login_required, current_user
app = Flask(__name__)

UPLOAD_FOLDER = 'result'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CORS(app)
app = Flask(__name__)
app.app_context().push()
app.secret_key = b'a secret key'

CORS(app)

@app.route('/')
def home():
    return render_template('index.html')


# IMPORT
@app.route('/import', methods=['POST'])
def view():
    try: 
        file = request.files['file']
        file.save(file.filename)

        filename = file.filename 
       
        variables_list = []
        with open(filename) as f: 
            for i , each_line in enumerate(f):
                edited  = each_line.replace("\\s+" , " ")
                temp_list = edited.split(" ")

                temp_new_list = []

                for each in temp_list:
                    if (each != ""):
                        temp_new_list.append(each.strip())

                for i in range(len(temp_new_list)-1):
                    item = temp_new_list[i]

                    if "MC" in item:
                        if len(item) > 3:
                            # SCENARIO 1: the "MC" is connected
                            index_of_MC = item.index("MC")
                            word_1 = item[0 : index_of_MC]
                            word_2 = item[index_of_MC : ]
                            new_item = word_1 + " " + word_2
                            temp_new_list[i] = new_item
                        else:
                            # SCENARIO 2: the "MC" is separated from the next itme
                            new_item = temp_new_list[i] + " " + temp_new_list[i + 1]
                            del temp_new_list[i+1]
                            temp_new_list[i] = new_item

                variables = (temp_new_list[0] , temp_new_list[1] , temp_new_list[2] , temp_new_list[3], temp_new_list[4])
                variables_list.append(variables)

            with open('result/results.txt', 'w') as writer:
                for each_var in variables_list:
                    writer.write('%-4s%-8s%-25s%-25s%-16s \n' % each_var)
            path = "./result/results.txt"

    except FileNotFoundError:
        print("File not Found")

    
    return send_file(path , as_attachment = True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=environ.get("PORT", 5000) ,debug=True)