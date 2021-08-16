from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from threading import Thread
from bot import CSG

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def root():
    params = dict(request.args)
    if params:
        jsonResp = {'ok' : True, 'message' : 'running programs'}
        Thread(target=lambda: openClientData(params), args=()).start()
        return jsonify(jsonResp)
    else:
        return jsonify({'ok' : False, 'message' : 'no params'})

def openClientData(clientData):
    b = CSG()
    b.login(clientData['login'], clientData['senha'])
    b.goToCsg()
    b.goToSign()
    b.addData(clientData)

app.run(host='localhost', port=5000)
