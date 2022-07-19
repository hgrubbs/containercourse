import pymysql.cursors
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.logger.setLevel('DEBUG')


def db_connect():
    connection = pymysql.connect(host='database', user='root', password='root', database='characters', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    return connection, cursor


@app.route('/', methods=['GET'])
def index():
    msg = {"hello": "mars"}
    return msg


@app.route('/names', methods=['GET'])
def names():
    connection, cursor = db_connect()
    cursor.execute("SELECT firstname, lastname FROM users;")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/absurd', methods=['GET'])
def absurd():
    connection, cursor = db_connect()
    cursor.execute("SELECT firstname, lastname FROM users WHERE (firstname='Zaphod' AND lastname='Beeblebrox');")
    result = cursor.fetchall()
    return jsonify(result)

