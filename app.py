from flask_cors import CORS
from flask import Flask, jsonify, request
import cx_Oracle

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}, supports_credentials=True)

username = 'NAVIERAUSER'
password = 'NavieraUser1'
dsn = cx_Oracle.makedsn('192.168.50.246', '1521', service_name='BD_NAVIERA')
connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)

@app.route('/consulta', methods=['GET'])
def consultar_datos():
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Cliente')
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500

@app.route('/register', methods=['POST', 'OPTIONS'])
def insertar_datos():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    req_data = request.json
    table_name = req_data.get('tabla')
    data = req_data.get('data')
    usuarioSistema = req_data.get('usuarioSistema')

    try:
        cursor = connection.cursor()
        placeholders = ', '.join([':' + str(i + 1) for i in range(len(data))])
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        query = f'INSERT INTO Cliente ({columns}) VALUES {values}'
        print(query)
        cursor.execute(query)
        placeholders = ', '.join([':' + str(i + 1) for i in range(len(usuarioSistema))])
        columns = ', '.join(usuarioSistema.keys())
        values = tuple(usuarioSistema.values())
        query = f'INSERT INTO Usuario_del_Sistema ({columns}) VALUES {values}'
        print(query)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        return jsonify({'message': 'Data inserted successfully'}), 201
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500

@app.route('/loguser', methods=['GET'])
def logUser():
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Cliente')
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        return jsonify({'error': str(error)}), 500

def _build_cors_preflight_response():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    app.run(debug=True)