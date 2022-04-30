from datetime import datetime
from flask import Flask, render_template, jsonify,request, make_response, abort
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

@app.route("/room", methods=['GET'])
def room():
    # userの登録処理
    if request.cookies.get('uid') is None:
        name='Anonymous'
        q_name = request.args.get("name")
        if q_name is None:
            name = q_name
        user = create_user(name)
    else:
        user = users[request.cookies.get('uid')]
    
    # roomに入る処理
    room_id = request.args.get("q")
    if room_id not in rooms:
        rooms[room_id] = {"users": [], "is_game_started": False} #TODO: roomがなければ作っちゃう, 本番でで消す
        # abort(400, 'this room not found') 
    in_room(user["user_id"], room_id)

    # roomがゲーム中か否かの処理
    if rooms[room_id]["is_game_started"] == True or request.args.get("start") is not None: #TODO: デバッグようなので後で消すstartがクエリパラメータに含まれていたらgame画面へ
        content = render_template("room_gaming.html", me=user)
    else:    
        content = render_template("room_waiting.html", me=user)

    # make_responseでレスポンスオブジェクトを生成する
    response = make_response(content)

    # Cookieの設定を行う
    max_age = 60 * 60 * 24 * 120 # 120 days
    expires = int(datetime.now().timestamp()) + max_age
    response.set_cookie('uid', value=str(user["user_id"]), max_age=max_age, expires=expires, secure=None, httponly=False)

    return response

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

#userの作成
def create_user(name):
    user_id = str(uuid.uuid4())
    user = {"user_id": user_id, "name": name,"room":None,"point":0}
    users[user_id] = user
    return user

#roomに入る処理
def in_room(user_id,room_id):
    if len(rooms[room_id]) == 4:
        abort(400, 'this room is empty') 
    # users[user_id]["room"]=room_id
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
    socketio.run(app, host='0.0.0.0', debug=True)
