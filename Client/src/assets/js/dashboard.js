import { createFlightCard, createTicketCardCancel } from './flightCard.js';
import { confirmIntent } from './intentConfirmation.js';

function handleKeyDown(event) {
    if (event.key === 'Enter') {
        onSendMessage();
    }
}

function handleWelcomeMessage(message) {
    let flagWelcome = false;
    const welcomeWords = [
        'שלום',
        'היי',
        'אהלן',
        'מה נשמע',
        'מה קורה',
        'מה הולך',
    ];

    if (welcomeWords.some((word) => message.includes(word))) {
        flagWelcome = true;
    }
    return flagWelcome;
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

    const flagWelcome = handleWelcomeMessage(val);

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

        confirmIntent(data, entities, flagWelcome);
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
        console.log('got a response');

        const parsedEntities = JSON.parse(entities);

        if (intent == 0) {
            console.log('you want to order');
            const flights = data.response;
            // Adding a message from server
            let chatMessages = document.getElementById('chat-messages');
            let newMessage = document.createElement('div');
            newMessage.className = 'message-back';
            // check if flights is empty
            if (flights.length == 0) {
                console.log('flights is empty');
                newMessage.textContent = 'לא נמצאו טיסות';
                chatMessages.appendChild(newMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } else if (!parsedEntities['Date2']) {
                console.log('flights is one way trip');
                newMessage.textContent = 'הנה כמה טיסות שמצאתי עבורך';
                chatMessages.appendChild(newMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                // create flight cards for each flight found
                flights.forEach((flight) => {
                    createFlightCard(flight);
                });
            } else {
                console.log('flights is round trip');
                newMessage.textContent = 'הנה כמה טיסות הלוך שמצאתי עבורך';
                chatMessages.appendChild(newMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                // create flight cards for each flight found
                let flights1 = flights[0];
                let flights2 = flights[1];
                console.log('flights1', flights1);
                flights1.forEach((flight) => {
                    createFlightCard(flight, flights2);
                });
            }
        }
        if (intent == 1) {
            const ticket = data.response;

            let chatMessages = document.getElementById('chat-messages');
            let newMessage = document.createElement('div');
            newMessage.className = 'message-back';

            if (ticket == null) {
                newMessage.textContent = 'לא נמצא כרטיס';
            } else {
                newMessage.textContent =
                    'הכרטיס נמצא בהצלחה, בחר בכרטיס כדי לבטלו';
            }

            chatMessages.appendChild(newMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            createTicketCardCancel(ticket);
        }
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
