var socket = io();
  const room_id = getParam("q")

  let users_in_room = {}

  const user_id = document.cookie
  .split('; ')
  .find(row => row.startsWith('uid'))
  .split('=')[1];

  console.log(user_id)

  socket.on('connect', function() {
    socket.emit('user_join', {room_id: room_id, user_id: user_id});
  });
  socket.on("message", function(message) {
    console.log(message)
    var li = document.createElement('li');
    li.innerHTML = message;
    document.getElementById("kazyougaki").appendChild(li)
  })

  // roomSocket = io.connect(`http://localhost:5000/room_id-${room_id}`);
  // roomSocket.on("connect", function() {
  //   console.log("room connected")
  // })

  socket.on("user_join", function(data) {
    console.log(data)
    //TODO: userのDOMを追加
    users_in_room = data
    documentCreateUsers()
  })

  socket.on("start_game", function() {
    // リロードすることでゲームを開始する
    location.reload();
  })

  function documentCreateUsers() {
    let members = document.getElementById("members")
    members.innerHTML = ''
    users_info = Object.values(users_in_room)
    users_info.map((user_info) => {
      let member = document.createElement("div")
      member.innerHTML = user_info["name"]
      member.classList.add("member-box")
      members.appendChild(member)
    })
    console.log(users_info)

    if (users_info.length == 4) {
      enableGameStartBtn()
    }
  }

  function enableGameStartBtn() {
    document.getElementById("game-start-btn").removeAttribute("disabled");
  }
  
  function gameStart() {
    socket.emit('start_game', room_id);
  }

function getParam(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
  }