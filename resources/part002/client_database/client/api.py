import pymysql.cursors
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.logger.setLevel('DEBUG')

@app.route('/', methods=['GET'])
def index():
    msg = {"hello": "world"}
    return msg

@app.route('/users', methods=['GET'])
def users():
    # Connect to the database
    connection = pymysql.connect(host='database',
                                 user='root',
                                 password='root',
                                 database='somedb',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    cursor.execute("SELECT firstname, lastname FROM users;")
    result = cursor.fetchall()
    return jsonify(result)
