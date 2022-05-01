const image_paths = ["/static/image/dan.png", "/static/image/dodon.png", "/static/image/gyaa.png", "/static/image/gaku.png", "/static/image/puru.png", "/static/image/pon.png", "/static/image/dondon.png", "/static/image/misimisi.png"]
let answerer_selected = ""

let questioner_selected_img = ""
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
  socket.on("receive_onomatopoeia", function(img_path) {
    var img = document.createElement('img');
    img.src = img_path;
    document.getElementById("onomatopoeia").appendChild(img)
    is_answered = false
    setCounter()
  })

  socket.on("start_game", function() {
    // リロードすることでゲームを開始する
    location.reload();
  })

  let is_answered = false
  socket.on("answered", function(data) {
    is_answered = true
    if (data["is_correct"]) {
      // まるまるさんが正解しました！次の問題へボタン
      let top = document.getElementById("top-text")
      top.innerHTML = `${data["user"]["name"]}さんが正解しました！正解は${data["answer"]}でした！`
      const button = document.createElement("button")
      button.innerHTML = '次の問題へ';
      console.log(button)
      button.onclick = function(){
        moveNextProblem()
      };
      document.getElementById("main-content").appendChild(button)
    } else {
      // まるまるさんがまるまるを洗濯しました。不正解です。
      let top = document.getElementById("top-text")
      // オノマトペを洗濯中。
      top.innerHTML = `${data["user"]["name"]}さん不正解！${data["answer"]}ではありません！`

      if (data["is_end"]) {
        top.innerHTML += `正解は${data["correct_answer"]}です！`
        const button = document.createElement("button")
        button.innerHTML = '次の問題へ';
        console.log(button)
        button.onclick = function(){
          moveNextProblem()
        };
        document.getElementById("main-content").appendChild(button)
      } else {
        top.innerHTML += "オノマトペ選択中"
      }
    }
  })

  socket.on("move_next", ()=>{
    location.reload()
  })

  function moveNextProblem() {
    fetch(`/next_problem?room_id=${room_id}`).then(response => response.json()).then((data) => {
      // TODO: 最後の問題の時の条件分岐
      console.log(data)
    })
  }

  function sendOnomatopoeia() {
    socket.emit('send_onomatopoeia', {img_path: questioner_selected_img, room_id: room_id})
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

function addOnomatopoeia(img_path) {
  images = document.getElementById("images")
  new_image = document.createElement("img")
  new_image.src = img_path
  images.appendChild(new_image)
}

function imgClick(selected_img_path) {
  questioner_selected_img = selected_img_path
  image_paths.map((image_path) => {
    console.log(image_path)
    const chosen_image =  document.getElementById(image_path)
    if (image_path == selected_img_path) {
      chosen_image.style.outline = "solid red"
    } else {
      chosen_image.style.outline = ""
    }
  })
}

function selected(pass) {
  const musics = document.getElementById("musics")
  const radioNodeList = musics.music 
  answerer_selected = radioNodeList.value

  radioNodeList.forEach(element => {
    element.disabled = "disabled"
  });

  document.getElementById("set-btn").disabled = true

  fetch(`/user_answer?room_id=${room_id}&user_id=${user_id}&selected_answer=${answerer_selected}`).then(response => response.json()).then((data) => {
    console.log(data)
    // socket.emit('start_game', room_id);
  })
}

function setCounter() {
  let top = document.getElementById("top-text")
  let timer = 60
  let timerId = setInterval(() => {
    if (timer <= 0 || is_answered) {
      clearInterval(timerId)
    } else {
      top.innerHTML = `残り時間 ${timer}s`
      timer--
    }
  }, 1000)
}
