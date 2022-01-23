# BY LUCA DIIORIO

from flask import Flask, render_template, request, url_for, redirect, Response, session, abort, send_from_directory, Response
from linear import *

# CONFIGURATION -------------------------------------------------
app = Flask(__name__)
app.config.update(DEBUG=True, SECRET_KEY='secretkeyverysecretalot')
# ---------------------------------------------------------------


# INDEX PAGE ----------------------------------------------------
@app.route('/')
def home():
    return render_template("index.html")
# ---------------------------------------------------------------


# API -----------------------------------------------------------
@app.route('/api/params', methods=['POST', 'GET'])
def modifica():

    if request.method == 'POST':
        data = request.json

        # process data
        print(data)
        with open("params.json", "w") as outfile:
            json.dump(data, outfile)

        _success = True
        return json.dumps({'success': _success}), 200, {'ContentType': 'application/json'}
    elif request.method == 'GET':
        with open("params.json") as json_data_file:
            data = json.load(json_data_file)
        return data

@app.route('/api/start', methods=['POST'])
def start():

    if request.method == 'POST':
        data = request.json
        if (data['start'] == 'true'):
            # start program
            ajson = runLinearCode()

        return json.dumps(ajson), 200, {'ContentType': 'application/json'}
# ---------------------------------------------------------------


#Entrega d'arxius estatics --------------------------------------
@app.route('/static/img/<path:path>')
def sendFileimg(path):
    return send_from_directory('static/img', path)

@app.route('/static/<path:path>')
def sendFile(path):
    return send_from_directory('static', path)
# ---------------------------------------------------------------


# RUN -----------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
# ---------------------------------------------------------------