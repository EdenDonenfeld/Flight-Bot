import { auth } from './firebase.js';
const { signInWithEmailAndPassword, onAuthStateChanged, createUserWithEmailAndPassword, signOut } = window.firebase;

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
    return signInWithEmailAndPassword(auth, email, password)
}

function logOut() {
    signOut(auth).then(() => {
        // Sign-out successful.
    }).catch((error) => {
        // An error happened.
    });
}

function getCurrentUser() {
    return auth.currentUser;
}

function setCallbackAuthChanged(callback){
    onAuthStateChanged(auth, (user) => {
        if (user) {
            callback(user)
        }
        else {
            callback(null)
        }
    })
}

window.signUp = signUp;
window.signIn = signIn;
window.signOut = logOut;
window.getCurrentUser = getCurrentUser;
window.setCallbackAuthChanged = setCallbackAuthChanged;