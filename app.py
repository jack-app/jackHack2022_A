from flask import Flask, render_template, jsonify
import uuid
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()
