from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = []

@app.route('/index')
def index():
    return render_template('index.html') # templatesフォルダ内のindex.htmlを表示する

@app.route('/user_create')
def user_create():
    user = { "user_id": uuid.uuid4(), "name": "name"} #TODO: フロントエンドからnameを受け取る。
    users.append(user)
    print(users)
    return jsonify(user_id=user["user_id"])

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
