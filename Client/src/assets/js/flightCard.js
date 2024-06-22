export function createFlightCard(flight) {   // flight is a flight object
    const flightCard = document.createElement('div');
    flightCard.className = 'card';
    const datetimeString = flight["Date"];
    const dateObj = new Date(datetimeString);
    console.log("Date: ", dateObj);
    let hours = dateObj.getHours();
    let minutes = dateObj.getMinutes();
    console.log("Hours: ", hours);
    console.log("Minutes: ", minutes);
    if (minutes < 10) {
        minutes = `0${minutes}`;
    }
    const departure = `${hours}:${minutes}`;
    const duration = flight["Duration"].split(":")[0];
    let arrivalHours = hours + parseInt(duration);
    let arrival = `${arrivalHours}:${minutes}`;
    if (arrivalHours > 24) {
        arrivalHours = arrivalHours - 24;
        arrival = `${arrivalHours}:${minutes}`;
    }
    
    flightCard.innerHTML = `
        <p class="departure"><strong>Departure:</strong> ${departure}</p>
        <p class="duration"><strong>Duration:</strong> ${flight["Duration"]}</p>
        <p class="arrival"><strong>Arrival:</strong> ${arrival}</p>
        <p class="origin"><strong>From:</strong> ${flight["Origin"]}</p>
        <p class="arrow">→</p>
        <p class="destination"><strong>To:</strong> ${flight["Destination"]}</p>
        <p class="price"><strong>Price:</strong> ${flight["Price"]}$ </p>
    `;

    const chatMessages = document.getElementById('chat-messages');
    chatMessages.appendChild(flightCard);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}