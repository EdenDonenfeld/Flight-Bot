import { auth } from './firebase.js';
const { signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } = window.firebase;

function signUp(email, password) {
    createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        // Signed up successfully
        var user = userCredential.user;
    })
    .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        // Handle errors
    });
}

function signIn(email, password) {
    console.log(auth)
    signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
        // Signed in successfully
        var user = userCredential.user;
        console.log(user)
    })
    .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        // Handle errors
    });
}

function logOut() {
    signOut(auth).then(() => {
        // Sign-out successful.
    }).catch((error) => {
        // An error happened.
    });
}

window.signUp = signUp;
window.signIn = signIn;
window.signOut = logOut;
