import { createFlightCard } from './flightCard.js';
// import { confirmIntent } from './intentConfirmation.js';

function handleKeyDown(event) {
  if (event.key === 'Enter') {
    onSendMessage();
  }
}

function onloadfunction(){
  let chatMessages = document.getElementById("chat-messages");
  let welcomeMessage = document.createElement('div');
  welcomeMessage.className = "message-back";
  welcomeMessage.textContent = "מה הולך? ברוך הבא לבוט הכי חברי שתכיר אי פעם! כל מה שתצטרך אני פה לעזור - מהזמנת טיסה עד לביטולה וכל מה שיש בינהם :)";
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
    const message = data.response;
    const predictedLabel = data.predicted_label;
    const responseData = data.response_data;
    const entities = data.entities;
    console.log('Entities', entities);

<<<<<<< HEAD

    let hebrewResponseData = "";
    if (responseData == "you want to order a ticket") {
      hebrewResponseData = "אני רוצה להזמין כרטיס";
    }
    else if (responseData == "you want to refund a ticket") {
      hebrewResponseData = "אני רוצה החזר על הכרטיס";
    }
    else if (responseData == "you want to check the status of your ticket") {
      hebrewResponseData = "אני רוצה לבדוק סטטוס של כרטיס";
    }
    else if (responseData == "you want to change the date of your ticket") {
      hebrewResponseData = "אני רוצה לשנות את התאריך של הכרטיס";
    }
    else if (responseData == "you want to change the destination of your ticket") {
      hebrewResponseData = "אני רוצה לשנות את היעד של הכרטיס";
    }
    else if (responseData == "you want to know the weather of your destination") {
      hebrewResponseData = "אני רוצה לדעת את המזג אוויר ביעד";
    }
    else if (responseData == "you want to know what is allowed in the flight") {
      hebrewResponseData = "אני רוצה לדעת מה מותר לעלות לטיסה";
=======
    let hebrewResponseData = '';
    if (responseData == 'you want to order a ticket') {
      hebrewResponseData = 'אני רוצה להזמין כרטיס';
    } else if (responseData == 'you want to refund a ticket') {
      hebrewResponseData = 'אני רוצה החזר על הכרטיס';
    } else if (responseData == 'you want to check the status of your ticket') {
      hebrewResponseData = 'אני רוצה לבדוק סטטוס של כרטיס';
    } else if (responseData == 'you want to change the date of your ticket') {
      hebrewResponseData = 'אני רוצה לשנות את התאריך של הכרטיס';
    } else if (
      responseData == 'you want to change the destination of your ticket'
    ) {
      hebrewResponseData = 'אני רוצה לשנות את היעד של הכרטיס';
    } else if (
      responseData == 'you want to know the weather of your destination'
    ) {
      hebrewResponseData = 'אני רוצה לדעת את המזג אוויר ביעד';
    } else if (
      responseData == 'you want to know what is allowed in the flight'
    ) {
      hebrewResponseData = 'אני רוצה לדעת מה מותר לעלות לטיסה';
>>>>>>> e69989ce44c263c2fdd8da522aa9bd6cc9cf210b
    }

    let intentVerifiedMessage = document.getElementById('chat-messages');
    let newIntentVerifiedMessage = document.createElement('div');
    newIntentVerifiedMessage.className = 'message-back';
    newIntentVerifiedMessage.textContent =
      'זיהיתי את ההודעה שלך כ: ' + hebrewResponseData + ', האם זו כוונתך?';
    intentVerifiedMessage.appendChild(newIntentVerifiedMessage);
    intentVerifiedMessage.scrollTop = intentVerifiedMessage.scrollHeight;

    let intentVerifiedRightMessage = document.getElementById('chat-messages');
    let newIntentVerifiedRightMessage = document.createElement('button');
    newIntentVerifiedRightMessage.className = 'message-back';
    newIntentVerifiedRightMessage.textContent = 'כן, זוהי כוונתי';
    newIntentVerifiedRightMessage.style.backgroundColor = 'green';
    newIntentVerifiedRightMessage.onclick = function () {
      const userConfirmed = true;
      console.log(userConfirmed);
      newIntentVerifiedRightMessage.disabled = true;
      newIntentVerifiedWrongMessage.disabled = true;
      validatedAction(predictedLabel, entities);
    };
    intentVerifiedRightMessage.appendChild(newIntentVerifiedRightMessage);
    intentVerifiedRightMessage.scrollTop =
      intentVerifiedRightMessage.scrollHeight;

    let intentVerifiedWrongMessage = document.getElementById('chat-messages');
    let newIntentVerifiedWrongMessage = document.createElement('button');
    newIntentVerifiedWrongMessage.className = 'message-back';
    newIntentVerifiedWrongMessage.textContent = 'לא, זוהי לא כוונתי';
    newIntentVerifiedWrongMessage.style.backgroundColor = 'red';
    newIntentVerifiedWrongMessage.onclick = function () {
      const userConfirmed = false;
      console.log(userConfirmed);
      newIntentVerifiedRightMessage.disabled = true;
      newIntentVerifiedWrongMessage.disabled = true;
    };
    intentVerifiedWrongMessage.appendChild(newIntentVerifiedWrongMessage);
    intentVerifiedWrongMessage.scrollTop =
      intentVerifiedWrongMessage.scrollHeight;

    // if (newIntentVerifiedWrongMessage.textContent = "לא, זוהי לא כוונתי") {
    // // הודעת נסח מחדש
    // }

    // Adding a message from server
    // let chatMessages = document.getElementById("chat-messages");
    // let newMessage = document.createElement('div');
    // newMessage.className = "message-back";
    // newMessage.textContent = message;
    // chatMessages.appendChild(newMessage);
    // chatMessages.scrollTop = chatMessages.scrollHeight;

    // if (predictedLabel == 0) {
    //   const flight = {
    //     "departure_time": "9:00",
    //     "origin": "TLV",
    //     "duration": "2:30",
    //     "arrival_time": "11:30",
    //     "destination": "ATH",
    //     "price": "200$"
    //   }
    //   createFlightCard(flight);
    // }
  } catch (error) {
    console.error('Error getting entities:', error);
  }
}
async function validatedAction(intent, entities) {
  console.log('Entities', entities);
  try {
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
<<<<<<< HEAD
  document.onload(onloadfunction())
  document.getElementById('submitButton').addEventListener('click', onSendMessage);
  document.getElementById('messageInput').addEventListener('keydown', handleKeyDown);
})
=======
  document
    .getElementById('submitButton')
    .addEventListener('click', onSendMessage);
  document
    .getElementById('messageInput')
    .addEventListener('keydown', handleKeyDown);
});
>>>>>>> e69989ce44c263c2fdd8da522aa9bd6cc9cf210b
