

const socket = new WebSocket("ws://localhost:8001/");

socket.onopen = function(e) {
  alert("[open] Connection established");
  alert("Sending to server");
  socket.send("My name is John");
};

function sendText() {
  // Создайте объект содержащий данные, необходимые серверу для обрабоки сообщения от клиента чата.
  var msg = {
    type: "message",
    text: document.getElementById("text").value,
    id:   clientID,
    date: Date.now()
  }

  // Отправьте объект в виде JSON строки.
  socket.send(JSON.stringify(msg));

  // Очистите элемент ввода текста, чтобы получить следующую строку текста от пользователя.
  document.getElementById("text").value = "";
};

socket.onmessage = function (event) {
  console.log(event.data);
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
  alert(`[error] ${error.message}`);
};