const image_paths = ["static/image/dan.png", "static/image/dodon.png", "static/image/gyaa.png", "static/image/gaku.png", "static/image/puru.png", "static/image/pon.png", "static/image/dondon.png", "static/image/misimisi.png"]
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
  })

  socket.on("start_game", function() {
    // リロードすることでゲームを開始する
    location.reload();
  })

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

  if (pass == "pass") {
    answerer_selected = pass
  }
  
  document.getElementById("set-btn").disabled = true
  document.getElementById("pass-btn").disabled = true

}