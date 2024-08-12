export function createFlightCard(flight) {
  // flight is a flight object
  const flightCard = document.createElement('div');
  flightCard.className = 'card';
  const datetimeString = flight['Date'];
  const dateObj = new Date(datetimeString);
  let hours = dateObj.getHours();
  let minutes = dateObj.getMinutes();
  if (minutes < 10) {
    minutes = `0${minutes}`;
  }
  const departure = `${hours}:${minutes}`;
  const duration = flight['Duration'].split(':')[0];
  let arrivalHours = hours + parseInt(duration);
  let arrival = `${arrivalHours}:${minutes}`;
  if (arrivalHours > 24) {
    arrivalHours = arrivalHours - 24;
    arrival = `${arrivalHours}:${minutes}`;
  }

  flightCard.innerHTML = `
        <p class="departure"><strong>המראה :</strong> ${departure}</p>
        <p class="duration"><strong>משך טיסה :</strong> ${flight['Duration']}</p>
        <p class="arrival"><strong>נחיתה :</strong> ${arrival}</p>
        <p class="origin"><strong>מ :</strong> ${flight['Origin']}</p>
        <p class="arrow">&larr;</p>
        <p class="destination"><strong>ל :</strong> ${flight['Destination']}</p>
        <p class="price"><strong>מחיר :</strong> ${flight['Price']}$ </p>
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

      addMessageBack('בחר מושבים עבור הטיסה');

      // create container for the seats
      const container = document.createElement('div');
      container.id = 'container';
      container.className = 'container';
      chatMessages.appendChild(container);

      createNextButton('הבא', flight);

      createSeatsContainer(flight.FlightNumber);
    }
  });
}

export function createTicketCardCancel(ticket) {
  createTicketCard(ticket, 'red');
  const ticketCard = document.querySelector('.ticket-card');
  ticketCard.addEventListener('click', () => {
    ticketCard.style.border = '1px solid red';
    // delete other ticket cards
    const cards = document.getElementsByClassName('ticket-card');
    for (let i = 0; i < cards.length; i++) {
      if (cards[i] !== ticketCard) {
        cards[i].remove();
      }
    }
  });
}

async function createSeatsContainer(flightNumber) {
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

  const avaliableSeats = await listenForSeats(flightNumber);

  createSeats(avaliableSeats);
}

async function listenForSeats(flightNumber) {
  try {
    // Await the fetch call
    const response = await fetch(`/api/seats/${flightNumber}`);

    // Check if the response is ok
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // Await the response data
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Error fetching seats:', error);
    throw error;
  }
}

function createSeats(avaliableSeats) {
  const rowsContainer = document.querySelector('.rows');
  const nextButton = document.querySelector('.next-button');

  // Function to create a single row
  function createRow(rowNumber) {
    const row = document.createElement('div');
    row.classList.add('row');

    for (let i = 0; i < 6; i++) {
      const column = document.createElement('div');
      column.classList.add('column');

      // Setting the ID of each column to its corresponding letter (A-F)
      column.id = rowNumber + String.fromCharCode(65 + i);

      // Creating a button for each seat
      const button = document.createElement('button');
      button.textContent = column.id;
      button.classList.add('seat');
      button.dataset.seatId = column.id;
      if (!avaliableSeats.includes(button.textContent)) {
        button.disabled = true;
        button.classList.add('disabled-seat');
      }

      button.addEventListener('click', function () {
        this.classList.toggle('selected');
        // Show next button if at least one seat is selected
        nextButton.style.display =
          document.querySelectorAll('.selected').length > 0 ? 'block' : 'none';
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
  let chatMessages = document.getElementById('chat-messages');
  let newMessage = document.createElement('div');
  newMessage.className = 'message-back';
  newMessage.textContent = message;
  chatMessages.appendChild(newMessage);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function createNextButton(message, flight) {
  let chatMessages = document.getElementById('chat-messages');
  let nextButton = document.createElement('button');
  nextButton.className = 'message-back next-button';
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
    selectedSeats.forEach((seat) => {
      seats.push(seat.dataset.seatId);
    });

    console.log(seats);
    // remove the seats container
    document.getElementById('container').remove();
    nextButton.remove();

    //sends the selected seats to the server
    sendSelectedSeats(seats, flight);
  });
}

async function sendSelectedSeats(seats, flight) {
  // console.log(flight);
  ///create the dictionary to send to the server named entities
  let entities = {
    seats: seats,
    user: window.user,
    label: 0,
    flight_num: flight.FlightNumber,
    flight: flight,
  };
  ///conver the dictionary to string
  entities = JSON.stringify(entities);
  try {
    const response = await fetch(`/api/finalActions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ entities: entities }),
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();
    const ticket = data.response;

    // Adding a message from server
    let chatMessages = document.getElementById('chat-messages');
    let newMessage = document.createElement('div');
    newMessage.className = 'message-back';
    // check if ticket is empty
    if (ticket.length == 0) {
      newMessage.textContent = 'לא ניתן להזמין כרטיסים';
    } else {
      newMessage.textContent = 'הכרטיס שהזמנת';
    }
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    createTicketCard(ticket, 'green');
  } catch (error) {
    console.error('Error getting ticket:', error);
  }
}

function createTicketCard(ticket, color) {
  // ticket is a Ticket object dictionary
  const ticketCard = document.createElement('div');
  ticketCard.className = 'ticket-card';
  const ticket_id = ticket['TicketID'];
  const flight_number = ticket['FlightNumber'];
  const seats = ticket['Seats'].join(', ');

  if (color === 'green') {
    ticketCard.classList.add('green');
  } else if (color === 'red') {
    ticketCard.classList.add('red');
  }

  ticketCard.innerHTML = `
    <p class="ticket-id"><strong>מספר כרטיס: </strong> ${ticket_id}</p>
    <p class="flight-number"><strong>מספר טיסה :</strong> ${flight_number}</p>
    <p class="seats"><strong>מושבים :</strong> ${seats}</p>
  `;

  const chatMessages = document.getElementById('chat-messages');
  chatMessages.appendChild(ticketCard);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
