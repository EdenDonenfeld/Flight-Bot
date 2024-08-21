import {
    getAuth,
    onAuthStateChanged,
} from 'https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js';

document.addEventListener('DOMContentLoaded', () => {
    const auth = getAuth();
    onAuthStateChanged(auth, (user) => {
        if (user) {
            const uid = user.uid;
            sendToServer(uid);

            // Your code to use the UID
        } else {
            // Redirect to login or show an error
            window.location.assign('/');
        }
    });
});

async function sendToServer(uid) {
    try {
        const response = await fetch('/api/myTickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'user-id': uid }),
        });
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}
