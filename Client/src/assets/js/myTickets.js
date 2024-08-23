import {
    getAuth,
    onAuthStateChanged,
} from 'https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js';

document.addEventListener('DOMContentLoaded', () => {
    const auth = getAuth();
    onAuthStateChanged(auth, async (user) => {
        if (user) {
            const uid = user.uid;
            const tickets = await sendToServer(uid);

            if (tickets.length === 0) {
                const ticketContainer =
                    document.querySelector('.tickets-container');
                const noTicketsElement = document.createElement('p');
                noTicketsElement.classList.add('no-tickets-msg');
                noTicketsElement.innerText = 'No tickets found';
                ticketContainer.appendChild(noTicketsElement);
            }

            tickets.forEach((ticket) => createTicket(ticket));

            // Your code to use the UID
        } else {
            // Redirect to login or show an error
            window.location.assign('/');
        }
    });
});

async function sendToServer(uid) {
    console.log(uid);
    try {
        const response = await fetch('/api/myTickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'user-id': uid }),
        });
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
    }
}

function createTicket(ticket) {
    const ticketContainer = document.querySelector('.tickets-container');
    const ticketElement = document.createElement('div');
    ticketElement.classList.add('ticket-card');
    ticketElement.classList.add('my-ticket');
    const ticket_id = ticket['TicketID'];
    const flight_number = ticket['FlightNumber'];
    const seats = ticket['Seats'].join(', ');
    ticketElement.innerHTML = `
        <p class="ticket-id" dir="rtl"><strong>מספר כרטיס: </strong> ${ticket_id}</p>
        <p class="flight-number" dir="rtl"><strong>מספר טיסה :</strong> ${flight_number}</p>
        <p class="seats" dir="rtl"><strong>מושבים :</strong> ${seats}</p>
    `;
    ticketContainer.appendChild(ticketElement);
}
