import { createFlightCard } from './flightCard.js';
import { confirmIntent } from './intentConfirmation.js';

function handleKeyDown(event) {
  if (event.key === 'Enter') {
    onSendMessage();
  }
}

function onloadfunction() {
  let chatMessages = document.getElementById('chat-messages');
  let welcomeMessage = document.createElement('div');
  welcomeMessage.className = 'message-back';
  welcomeMessage.textContent =
    'מה הולך? ברוך הבא לבוט הכי חברי שתכיר אי פעם! כל מה שתצטרך אני פה לעזור - מהזמנת טיסה עד לביטולה וכל מה שיש בינהם :)';
  chatMessages.appendChild(welcomeMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;
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
    let chatMessages = document.getElementById('chat-messages');
    let newMessage = document.createElement('div');
    newMessage.className = 'message';
    newMessage.textContent = val;
    chatMessages.appendChild(newMessage);
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  console.log('Message', val);

  try {
    const response = await fetch(`/api/flightbot`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: val, user_id: window.user }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    const entities = data.entities;
    console.log('Entities', entities);

    confirmIntent(data, entities);
  } catch (error) {
    console.error('Error getting entities:', error);
  }
}
export async function validatedAction(intent, entities) {
  try {
    console.log('Intent: ', intent);
    console.log('Entities: ', entities);
    const response = await fetch(`/api/valflightbot`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        entities: entities,
        label: intent,
        user: window.user,
      }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    const flights = data.response;

    console.log('Data: ', data);
    console.log('Flights: ', flights);

    // Adding a message from server
    let chatMessages = document.getElementById('chat-messages');
    let newMessage = document.createElement('div');
    newMessage.className = 'message-back';
    // check if flights is empty
    if (flights.length == 0) {
      newMessage.textContent = 'לא נמצאו טיסות';
    } else {
      newMessage.textContent = 'הנה כמה טיסות שמצאתי עבורך';
    }
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    // create flight cards for each flight found
    console.log('Flights:', flights);
    let counter = 1;
    flights.forEach((flight) => {
      createFlightCard(flight);
    });
  } catch (error) {
    console.error('Error getting entities:', error);
  }
}

document.addEventListener('DOMContentLoaded', function () {
  window.onload = onloadfunction;
  document
    .getElementById('submitButton')
    .addEventListener('click', onSendMessage);
  document
    .getElementById('messageInput')
    .addEventListener('keydown', handleKeyDown);
});
