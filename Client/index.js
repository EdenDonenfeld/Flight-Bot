async function onSendMessage() {
  const input = document.getElementById('messageInput')
  const response = await fetch(`http://localhost:3000/api/flightbot/${input.value}`, {
    method: 'POST'
  });
  const message = await response.text();
  const result = document.getElementById('result');
  result.textContent = message;
}