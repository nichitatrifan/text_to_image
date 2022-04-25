let socket = new WebSocket("ws://127.0.0.1:5051/");
let count = 0

socket.onopen = function(e) {
  //alert("[open] Connection established");
  //alert("Sending to server");
  //socket.send("My name is John");
  console.log('connection established!')
  //sendText()
  let chatName = JSON.parse(sessionStorage.getItem("chatName"));
  if (chatName != "") document.getElementById('chat-title').innerHTML = "<strong>"+chatName+"</strong>";
};

function sendText() {
  // Создайте объект содержащий данные, необходимые серверу для обрабоки сообщения от клиента чата.
  let message = document.getElementById('text-input').value
  if (message != "") {
    let encodedMessage = encodeMessage()
    if (encodedMessage != null) {
      var msg = {
        type: "message",
        text: encodedMessage,
        count: count,
        date: Date.now()
      }

      // Отправьте объект в виде JSON строки.
      socket.send(JSON.stringify(msg));
      count++
      document.getElementById("chat-content").innerHTML += "<div class=\"media media-chat\"><div class=\"media-body\"><p>" + message + "</p></div></div>";
    }
    else {
      alert('Invalid Message');
    }
    // Очистите элемент ввода текста, чтобы получить следующую строку текста от пользователя.
    // document.getElementById("text").value = "";
    document.getElementById("text-input").value = "";
  }
};

socket.onmessage = function (event) {
  console.log(event.data);
  if (event.data.startsWith("{\"type\": \"message\"")){
    let data = JSON.parse(event.data);
    receiveMessage(data["text"]);
  };
}

socket.onclose = function(event) {
  if (event.wasClean) {
    alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    // e.g. server process killed or network down
    // event.code is usually 1006 in this case
    alert('[close] Connection died');
  }
};

socket.onerror = function(error) {
  //alert(`[error] ${error.message}`);
  console.log(error.message)
};

document.getElementById('text-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    sendText()
  }
});
