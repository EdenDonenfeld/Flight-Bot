export function createFlightCard(flight) {   // flight is a flight object
    const flightCard = document.createElement('div');
    flightCard.className = 'card';
  
    flightCard.innerHTML = `
        <p class="departure"><strong>Departure:</strong> ${flight.departure_time}</p>
        <p class="duration"><strong>Duration:</strong> ${flight["Duration"]}</p>
        <p class="arrival"><strong>Arrival:</strong> ${flight.arrival_time}</p>
        <p class="origin"><strong>From:</strong> ${flight["Origin"]}</p>
        <p class="arrow">→</p>
        <p class="destination"><strong>To:</strong> ${flight["Destination"]}</p>
        <p class="price"><strong>Price:</strong> $${flight["Price"]} </p>
    `;

    const chatMessages = document.getElementById('chat-messages');
    chatMessages.appendChild(flightCard);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}