from flask import Flask, render_template, jsonify,request
from flask_socketio import SocketIO, send, emit
import uuid
import random
import copy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user_count = 0
users = {}
rooms={}
musics=[]
onomatope=[]

@app.route('/index')
def index():
    return render_template('index.html') # templatesフォルダ内のindex.htmlを表示する

#ユーザーを作成
@app.route('/user_create')
def user_create():
    name='Anonymous'
    try:
        req = request.args
        name = req.get("name")
    except:
        pass
    user_id = uuid.uuid4()
    users[user_id]={"name": name,"room":None,"point":0}
    print(users)
    return jsonify(user_id=user_id)

#ルームを作成
@app.route('/room_create')
def room_create():
    room_id = uuid.uuid4()
    rooms[room_id]={ "users":[],"questioner_id":"","answerer_id":[],"answer":""} 

#解答の判定
@app.route('/user_answer')
def user_answer():
    req = request.args
    user_id = req.get("user_id")
    answer=req.get('answer')
    if answer==rooms[users[user_id]["room"]]['answer']:
        users[user_id]["point"]+=1
    return jsonify(right_or_wrong=(answer==rooms[users[user_id]["room"]]['answer']))

#オノマトペの選択
@app.route('/select_onomatopoeia')
def select_onomatopoeia(onmatopoeia):
    return 

#roomに入る処理
def in_room(user_id,room_id):
    users[user_id]["room"]=room_id
    rooms[room_id]["users"].append(user_id)

#roomから出る処理
def out_room(user_id,room_id):
    users[user_id]["room"]=None
    rooms[room_id]["users"].remove(user_id)

#出題者、回答者を決める
@app.route('/select_answerer')
def  select_answerer():
    req = request.args
    room_id = req.get("rooom_id")
    users=rooms[room_id]["users"].copy()
    questioner_id=users.pop()
    rooms[room_id]["questioner_id"]=questioner_id
    rooms[room_id]["answererer_id"]=users
    return jsonify(questioner_id=questioner_id,answerer_id=users)

#お題と選択肢を決める
@app.route('/select_problem')
def select_problem():
    req = request.args
    room_id = req.get("rooom_id")
    answer=random.choice(musics)
    choices=[]
    while choices!=[]:
        choice=random.sample(musics,3)
        if answer not in choice:
            choices=choice
    choices.insert(random.randint(0,4))
    rooms[room_id]["answer"]=answer
    return jsonify(answer=answer,choices=choices)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
