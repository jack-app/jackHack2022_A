from datetime import datetime
from flask import Flask, render_template, jsonify,request, make_response, abort
from flask_socketio import SocketIO, send, emit, join_room
import uuid
import random
import os
from faker import Faker

fake = Faker()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user_count = 0
users = {}
rooms={}
musics=musics =[
{"name": "怪盗",   "id": "https://www.youtube.com/embed/rwkLzrK5GLA" },
{"name": "きらり", "id": "https://www.youtube.com/embed/IFCDLIKSArs"},
{"name": "怪物",   "id": "https://www.youtube.com/embed/qivRUhepWVA"},
{"name": "YOKAZE",     "id": "https://www.youtube.com/embed/q09Gs6e5XVI"},
{"name": "もう少しだけ", "id": "https://www.youtube.com/embed/VfATdDI3604"},
{"name": "ペテルギウス", "id": "https://www.youtube.com/embed/cbqvxDTLMps"},
{"name": "ドライフラワー", "id": "https://www.youtube.com/embed/X-YtmD0YsBA" },
{"name": "Lemon", "id": "https://www.youtube.com/embed/SX_ViT4Ra7k"},
{"name": "Happiness", "id": "https://www.youtube.com/embed/HeXVJvEYynw"},
{"name": "さよならエレジー", "id": "https://www.youtube.com/embed/XSkpuDseenY"},
{"name": "天体観測", "id": "https://www.youtube.com/embed/j7CDb610Bg0"},
{"name": "マリーゴールド", "id": "https://www.youtube.com/embed/0xSiBpUdW4E" },
{"name": "勿忘", "id": "https://www.youtube.com/embed/zkZARKFuzNQ"},
{"name": "CITRUS", "id": "https://www.youtube.com/embed/ye1YacA8HvE" },
{"name": "裸の心", "id": "https://www.youtube.com/embed/yOAwvRmVIyo"},
{"name": "虹", "id": "https://www.youtube.com/embed/hkBbUf4oGfA"},
{"name": "ギラギラ", "id": "https://www.youtube.com/embed/sOiMD45QGLs"},
{"name": "うっせぇわ", "id": "https://www.youtube.com/embed/Qp3b-RXtz4w" },
{"name": "カイト", "id": "https://www.youtube.com/embed/mTMs1S5td74"},
{"name": "YELL", "id": "https://www.youtube.com/embed/lz8frtP6_kk"},
{"name": "SAKURA", "id": "https://www.youtube.com/embed/61z-cqg28R8"},
{"name": "猫", "id": "https://www.youtube.com/embed/TwiEL7bUmAI" },
{"name": "奏", "id": "https://www.youtube.com/embed/J5Z7tIq7bco"},
{"name": "ボクノート", "id": "https://www.youtube.com/embed/AeMRXJtg500"},
{"name": "桜坂",         "id": "https://www.youtube.com/embed/AGYJ6jeu3p8"},
{"name": "家族になろうよ", "id": "https://www.youtube.com/embed/vrkbf9CVkn4"},
{"name": "恋",           "id": "https://www.youtube.com/embed/jhOVibLEDhA"},
{"name":"新宝島","id":"https://www.youtube.com/embed/LIlZCmETvsY"},
{"name":"前前前世","id":"https://www.youtube.com/embed/PDSkFeMVNFs"},
{"name":"シルエット","id":"https://www.youtube.com/embed/ZFoJYI7Q4iA"},
{"name":"インフェルノ","id":"https://www.youtube.com/embed/wfCcs0vLysk"},
{"name":"廻廻奇譚","id":"https://www.youtube.com/embed/1tk1pqwrOys" },
{"name":"白日","id":"https://www.youtube.com/embed/ony539T074w" },
{"name":"シャルル","id":"https://www.youtube.com/embed/VUIEJu4ZSUo"},
{"name": "Call Me Maybe", "id": "https://www.youtube.com/embed/fWNaR-rxAic"},
{"name": "初心LOVE" , "id": "https://www.youtube.com/embed/qNrRnnG8glY"},
{"name": "ロマンスの神様" , "id": "https://www.youtube.com/embed/T8yZWCg85Cs"},
{"name": "気まぐれロマンティック" , "id": "https://www.youtube.com/embed/5XCSt_0lwOE"},
{"name": "ヘビーローテーション" , "id": "https://www.youtube.com/embed/lkHlnWFnA0c"},
{"name": "勇気りんりん" , "id": "https://www.youtube.com/embed/GRG9WlqRfWY"},
]
image_paths=["/static/image", "/static/image/image (5).png", "/static/image/image (10).png", "/static/image/image (9).png", "/static/image/dan.png", "/static/image/dodon.png", "/static/image/image (8).png", "/static/image/image (11).png", "/static/image/image (4).png", "/static/image/image (16).png", "/static/image/gyaa.png", "/static/image/gaku.png", "/static/image/puru.png", "/static/image/image (20).png", "/static/image/image (3).png", "/static/image/image (21).png", "/static/image/image (2).png", "/static/image/pon.png", "/static/image/image (17).png", "/static/image/image (14).png", "/static/image/dondon.png", "/static/image/image (1).png", "/static/image/image (22).png", "/static/image/image (18).png", "/static/image/image (19).png", "/static/image/image (23).png", "/static/image/image (15).png", "/static/image/image (7).png", "/static/image/image (12).png", "/static/image/image (13).png", "/static/image/misimisi.png", "/static/image/image (6).png"]

@app.route('/index')
def index():
    return render_template('index.html') # templatesフォルダ内のindex.htmlを表示する

@app.route("/room", methods=['GET'])
def room():
    # userの登録処理
    if request.cookies.get('uid') is None:
        name=fake.name()
        q_name = request.args.get("name")
        if q_name is not None:
            name = q_name
        user = create_user(name)
    else:
        q_name = request.args.get("name")
        if q_name is not None:
            users[request.cookies.get('uid')]["name"] = q_name
        user = users[request.cookies.get('uid')]
    
    # roomに入る処理
    room_id = request.args.get("q")
    if room_id not in rooms:
        #TODO: 最初にstart_gameされたタイミングでgame_countをインクリメント。毎回選択肢が変われば成功。
        #TODO: answerを追加しないと。
        rooms[room_id] = {"users": [], "is_game_started": False, "game_count": 0, "games": [{"music_choices": random.sample(musics, 4), "choice_count": 0},{"music_choices": random.sample(musics, 4), "choice_count": 0},{"music_choices": random.sample(musics, 4), "choice_count": 0},{"music_choices": random.sample(musics, 4), "choice_count": 0},{"music_choices": random.sample(musics, 4)},]} #TODO: roomがなければ作っちゃう, 本番でで消す # ゲームの数は現状最大五個
        # abort(400, 'this room not found') 
    in_room(user, room_id)

    current_room = rooms[room_id]
    members = rooms[room_id]["users"]
    # print(members)

    # roomがゲーム中か否かの処理
    if rooms[room_id]["is_game_started"] == True or request.args.get("start") is not None: #TODO: デバッグようなので後で消すstartがクエリパラメータに含まれていたらgame画面へ
        is_questioner = False
        current_game = rooms[room_id]["game_count"]

        if current_room["games"][current_game]["questioner"]["user_id"] == user["user_id"]:
            is_questioner = True
        content = render_template("room_gaming.html", members=members, me=user, questioner=current_room["games"][current_game]["questioner"], music_choices=current_room["games"][current_game]["music_choices"],answer=current_room["games"][current_game]["answer"], is_questioner=is_questioner, image_paths=image_paths)
    else:    
        content = render_template("room_waiting.html", members=members,me=user, room_id=room_id)

    # make_responseでレスポンスオブジェクトを生成する
    response = make_response(content)

    # Cookieの設定を行う
    max_age = 60 * 60 * 24 * 120 # 120 days
    expires = int(datetime.now().timestamp()) + max_age
    response.set_cookie('uid', value=str(user["user_id"]), max_age=max_age, expires=expires, secure=None, httponly=False)

    return response

# #ルームを作成
# @app.route('/room_create')
# def room_create():
#     room_id = uuid.uuid4()
#     rooms[room_id]={ "users":[],"questioner_id":"","answerer_id":[],"answer":""} 

#解答の判定
@app.route('/user_answer')
def user_answer():
    req = request.args
    user_id = req.get("user_id")
    room_id = req.get("room_id")
    user = users[user_id]
    room = rooms[room_id]
    game_count = room["game_count"]
    selected_answer_id = req.get('selected_answer')
    correct_answer_id = room["games"][game_count]['answer']["id"]
    rooms[room_id]["games"][game_count]['choice_count'] += 1
    if selected_answer_id==correct_answer_id:
        users[user_id]["point"]+=1

    is_end = False
    # print(rooms[room_id]["games"][game_count]['choice_count'])
    if rooms[room_id]["games"][game_count]['choice_count'] == 3:
        is_end = True
    selected_answer = next(item for item in musics if item["id"] == selected_answer_id)
    correct_answer = room["games"][game_count]['answer']
    socketio.emit('answered', {'user': user, "answer": selected_answer, "is_correct": (selected_answer_id==correct_answer_id), "is_end": is_end, "correct_answer": correct_answer}, to=room_id, broadcast=True)
    return jsonify(right_or_wrong=(selected_answer==correct_answer))

#次の問題に移動
@app.route('/next_problem')
def next_problem():
    req=request.args
    room_id=req.get("room_id")
    if rooms[room_id]["game_count"]==4:
        return jsonify(users=users)
    rooms[room_id]["game_count"]+=1
    socketio.emit("move_next", to=room_id, broadcast=True)
    return jsonify(hoge="users")



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
def in_room(user,room_id):
    if user in rooms[room_id]["users"]:
        return
    if len(rooms[room_id]["users"]) >= 4:
        abort(400, 'this room is full') 
    # users[user]["room"]=room_id
    rooms[room_id]["users"].append(user)

# roomのゲームを開始する処理
def room_start_game(room_id):
    rooms[room_id]["is_game_started"] = True

# #TODO: 回答を集計する
# def calc_answer(room_id, answers):
#     rooms[room_id]["game_count"] += 1
#     print(answers)

#roomから出る処理
def out_room(user_id,room_id):
    users[user_id]["room"]=None
    rooms[room_id]["users"].remove(user_id)

#出題者、回答者を決める
@app.route('/make_games', methods=['GET'])
def  make_games():
    req = request.args
    room_id = req.get("q")
    room = rooms[room_id]
    for idx, game in enumerate(room["games"]):
        user_candidate_id = random.choice(room["users"])
        rooms[room_id]["games"][idx]["questioner"]=user_candidate_id
        rooms[room_id]["games"][idx]["answer"]=random.sample(game["music_choices"], 1)[0]
    return jsonify(room_id=room_id)

# #お題と選択肢を決める
# @app.route('/select_problem')
# def select_problem():
#     req = request.args
#     room_id = req.get("rooom_id")
#     answer=random.choice(musics)
#     choices=[]
#     while choices!=[]:
#         choice=random.sample(musics,3)
#         if answer not in choice:
#             choices=choice
#     choices.insert(random.randint(0,4))
#     rooms[room_id]["answer"]=answer
#     return jsonify(answer=answer,choices=choices)

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
    room_id = data["room_id"]
    join_room(room_id)
    emit("user_join",users,to=room_id,broadcast=True)

@socketio.on('start_game')
def start_game(room_id):
    room_start_game(room_id)
    emit("start_game",{"data":""},to=room_id,broadcast=True)

@socketio.on('send_onomatopoeia')
def send_onomatopoeia(data):
    emit("receive_onomatopoeia", data["img_path"],to=data["room_id"],broadcast=True)

def test_result(room_id):
    emit("game_result",{'data':[users[user_id]["point"]for user_id in rooms[room_id]]},broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=int(os.environ.get('PORT', 5000)))
