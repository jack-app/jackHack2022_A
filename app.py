from datetime import datetime
from flask import Flask, render_template, jsonify,request, make_response, abort
from numpy import broadcast
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
musics=["https://www.youtube.com/embed/rwkLzrK5GLA", "https://www.youtube.com/embed/IFCDLIKSArs", "https://www.youtube.com/embed/qivRUhepWVA", "https://www.youtube.com/embed/q09Gs6e5XVI", "https://www.youtube.com/embed/VfATdDI3604"] # もう少しだけまで https://www.youtube.com/embed/fxE176w8Z90
onomatope=["/static/image/dan.png", "/static/image/dodon.png", "/static/image/gyaa.png", "/static/image/gaku.png", "/static/image/puru.png", "/static/image/pon.png", "/static/image/dondon.png", "/static/image/misimisi.png"]

@app.route('/index')
def index():
    return render_template('index.html') # templatesフォルダ内のindex.htmlを表示する

@app.route("/room", methods=['GET'])
def room():
    # userの登録処理
    if request.cookies.get('uid') is None:
        name='Anonymous'
        q_name = request.args.get("name")
        if q_name is not None:
            name = q_name
        user = create_user(name)
    else:
        user = users[request.cookies.get('uid')]
    
    # roomに入る処理
    room_id = request.args.get("q")
    if room_id not in rooms:
        #TODO: 最初にstart_gameされたタイミングでgame_countをインクリメント。毎回選択肢が変われば成功。
        rooms[room_id] = {"users": [], "is_game_started": False, "game_count": 0, "games": [{"music_choices": random.sample(musics, 4)},{"music_choices": random.sample(musics, 4)},{"music_choices": random.sample(musics, 4)},{"music_choices": random.sample(musics, 4)},{"music_choices": random.sample(musics, 4)},]} #TODO: roomがなければ作っちゃう, 本番でで消す # ゲームの数は現状最大五個
        # abort(400, 'this room not found') 
    in_room(user["user_id"], room_id)

    # roomがゲーム中か否かの処理
    if rooms[room_id]["is_game_started"] == True or request.args.get("start") is not None: #TODO: デバッグようなので後で消すstartがクエリパラメータに含まれていたらgame画面へ
        room = rooms[room_id]
        user_candidate_id = random.choice(room["users"])
        user_candidate = users[user_candidate_id]
        music_choices = room["games"][room["game_count"]]["music_choices"]
        print(music_choices)
        content = render_template("room_gaming.html", me=user, questioner=user_candidate, music_choices=music_choices)
    else:    
        content = render_template("room_waiting.html", me=user, room_id=room_id)

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
    if user_id in rooms[room_id]["users"]:
        return
    if len(rooms[room_id]["users"]) == 4:
        abort(400, 'this room is full') 
    # users[user_id]["room"]=room_id
    rooms[room_id]["users"].append(user_id)

# roomのゲームを開始する処理
def room_start_game(room_id):
    rooms[room_id]["is_game_started"] = True
    rooms[room_id]["game_count"] += 1


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
    emit("message", data, broadcast=True)

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    print("connected")
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('user_join')
def user_join(data):
    print(users)
    emit("user_join",users,namespace=f'/room_id-{data["room_id"]}',broadcast=True)

@socketio.on('start_game')
def start_game(room_id):
    room_start_game(room_id)
    emit("start_game",{"data":""},namespace=f'/room_id-{room_id}',broadcast=True)


def test_result(room_id):
    emit("game_result",{'data':[users[user_id]["point"]for user_id in rooms[room_id]]},broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
