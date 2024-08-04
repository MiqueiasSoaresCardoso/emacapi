import ssl
from flask import Flask, jsonify, request
from pymongo import MongoClient
import os
import sys

from flask_cors import CORS

# Configuração da conexão com MongoDB Atlas
uri = "mongodb+srv://miqueiassoares:pMmAke6bpsOI8u6T@cluster0.sjuug1b.mongodb.net/Obmep"
client = MongoClient(uri, ssl=True)
db = client['EMAC']
collection = db['Inscritos']

app = Flask(__name__)
CORS(app)
# ENDPOINTS GERAIS
@app.route('/emac/inscricoes', methods=['POST'])
def inscricoes():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Erro ao inserir dados'}), 400

    #dados do usuário
    name = data['name']
    age = data['age']
    email = data['email']
    phone = data['phone']
    church = data['church']
    shepherd = data['shepherd']

    # Inserir novo usuário
    user_id = collection.insert_one({
        'name': name,
        'age': age,
        'email': email,
        'phone': phone,
        'church': church,
        'shepherd': shepherd,
    }).inserted_id

    return jsonify({'message': 'Dados Salvos com Sucesso'}), 200

@app.route('/emac/lista', methods=['GET'])
def listar():
    try:
        inscricoes = list(collection.find({}, {'_id': 0}))
        return jsonify(inscricoes), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao listar inscrições', 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(sys.path)
    app.run(host='0.0.0.0', port=port, debug=True)