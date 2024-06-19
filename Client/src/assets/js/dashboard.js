// import { createFlightCard } from './flightCard.js';

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

  // console.log(window.user);
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
      body: JSON.stringify({ message: val, user: window.user})
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    const message = data.response;
    const predictedLabel = data.predicted_label;
    const responseData = data.response_data;
    const entities = data.entities;
    
    ///confirmation message
    const userConfirmed = confirm("I interpreted your message as: " + responseData + ". Is this correct?");
    console.log(userConfirmed);

    
    // Adding a message from server
    let chatMessages = document.getElementById("chat-messages");
    let newMessage = document.createElement('div');
    newMessage.className = "message-back";
    newMessage.textContent = message;
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    if (userConfirmed) {
      validatedAction(predictedLabel, entities);
    }
  }
  catch (error) {
    console.error('Error getting entities:', error);
  }
}


async function validatedAction(intent, entities) {
  console.log("Entities", entities);
  try {
    const response = await fetch(`/api/valflightbot`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ entities: entities, label: intent, user: window.user})
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    const flights = data.response;

    // Adding a message from server
    let chatMessages = document.getElementById("chat-messages");
    let newMessage = document.createElement('div');
    newMessage.className = "message-back";
    newMessage.textContent = flights[0]["FlightNumber"];
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  
  }
  catch (error) {
    console.error('Error getting entities:', error);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('submitButton').addEventListener('click', onSendMessage);
  document.getElementById('messageInput').addEventListener('keydown', handleKeyDown);
})

