async function onSendMessage() {
  const input = document.getElementById('messageInput');
  
  if (!input.value) {
    return;
  }

  var val = input.value;
  console.log(val);

  if (val.trim() != '') {
    // Adding a message from client
    var chatMessages = document.getElementById("chat-messages");
    var newMessage = document.createElement('div');
    newMessage.className = "message";
    newMessage.textContent = val;
    chatMessages.appendChild(newMessage);
    input.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  

  const response = await fetch(`http://localhost:3000/api/flightbot/${val}`, {
    method: 'POST'
  });
  const message = await response.text();

  // Adding a message from server
  var chatMessages = document.getElementById("chat-messages");
  var newMessage = document.createElement('div');
  newMessage.className = "message-back";
  newMessage.textContent = message;
  chatMessages.appendChild(newMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}