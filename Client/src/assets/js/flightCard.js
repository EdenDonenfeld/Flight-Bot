export function createFlightCard(flight) {   // flight is a flight object
    const flightCard = document.createElement('div');
    flightCard.className = 'card';
    const datetimeString = flight["Date"];
    const dateObj = new Date(datetimeString);
    let hours = dateObj.getHours();
    let minutes = dateObj.getMinutes();
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

    let isFirstClick = true;

    // add click event listener to the card
    flightCard.addEventListener('click', () => {
        flightCard.style.border = '1px solid green';
        // delete other flight cards
        const cards = document.getElementsByClassName('card');
        for (let i = 0; i < cards.length; i++) {
            if (cards[i] !== flightCard) {
                cards[i].remove();
            }
        }

        if (isFirstClick) {
            isFirstClick = false;

            addMessageBack("בחר מושבים עבור הטיסה");

            // create container for the seats
            const container = document.createElement('div');
            container.id = 'container';
            container.className = 'container';
            chatMessages.appendChild(container);

            createNextButton("הבא");

            createSeatsContainer();

        }
    });
}

function createSeatsContainer() {
    const container = document.getElementById('container');
    container.innerHTML = `
        <div class="plane">
            <!-- Wings -->
            <div class="wing left"></div>
            <div class="wing right"></div>
            
            <!-- Rows will be dynamically added here -->
            <div class="rows"></div>
        </div>
    `;
    createSeats();
}

function createSeats() {
    const rowsContainer = document.querySelector(".rows");
    const nextButton = document.querySelector('.next-button');

    // Function to create a single row
    function createRow(rowNumber) {
        const row = document.createElement("div");
        row.classList.add("row");
        
        for (let i = 0; i < 6; i++) {
            const column = document.createElement("div");
            column.classList.add("column");

            // Setting the ID of each column to its corresponding letter (A-F)
            column.id = rowNumber + String.fromCharCode(65 + i);

            // Creating a button for each seat
            const button = document.createElement("button");
            button.textContent = column.id;
            button.classList.add("seat");
            button.dataset.seatId = column.id;

            button.addEventListener("click", function() {
                this.classList.toggle("selected");
                // Show next button if at least one seat is selected
                nextButton.style.display = document.querySelectorAll('.selected').length > 0 ? 'block' : 'none';
            });

            column.appendChild(button);
            row.appendChild(column);
        }
        
        rowsContainer.appendChild(row);
    }

    function createRows() {
        let numberOfRows = 5;
        for (let i = 1; i <= numberOfRows; i++) {
            createRow(i);
        }
    }

    createRows();
}

function addMessageBack(message) {
     // add a message to the chat
     let chatMessages = document.getElementById("chat-messages");
     let newMessage = document.createElement('div');
     newMessage.className = "message-back";
     newMessage.textContent = message;
     chatMessages.appendChild(newMessage);
     chatMessages.scrollTop = chatMessages.scrollHeight;
}


function createNextButton(message) {
    let chatMessages = document.getElementById("chat-messages");
    let nextButton = document.createElement('button');
    nextButton.className = "message-back next-button";
    nextButton.style.display = 'none';
    nextButton.textContent = message;
    chatMessages.appendChild(nextButton);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    nextButton.addEventListener('click', () => {
        const selectedSeats = document.querySelectorAll('.selected');
        if (selectedSeats.length === 0) {
            addMessageBack('בחר לפחות מושב אחד');
            return;
        }

        const seats = [];
        selectedSeats.forEach(seat => {
            seats.push(seat.dataset.seatId);
        });

        console.log(seats);
    });

}