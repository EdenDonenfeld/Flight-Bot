function handleKeyDown(event) {
  if (event.key === 'Enter') {
      onSendMessage();
  }
}

async function onSendMessage() {
  const input = document.getElementById('messageInput');
  
  if (!input.value) {
    return;
  }

  let val = input.value;

  if (val.trim() != '') {
    // Adding a message from client
    let chatMessages = document.getElementById("chat-messages");
    let newMessage = document.createElement('div');
    newMessage.className = "message";
    newMessage.textContent = val;
    chatMessages.appendChild(newMessage);
    input.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  console.log("Message", val);

  try {
    const response = await fetch(`/api/flightbot`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: val })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    const message = data.response;

    // Adding a message from server
    let chatMessages = document.getElementById("chat-messages");
    let newMessage = document.createElement('div');
    newMessage.className = "message-back";
    newMessage.textContent = message;
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
  catch (error) {
    console.error('Error:', error);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('submitButton').addEventListener('click', onSendMessage);
  document.getElementById('messageInput').addEventListener('keydown', handleKeyDown);
})