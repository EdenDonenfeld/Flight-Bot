import { auth } from './firebase.js';
const { signInWithEmailAndPassword, onAuthStateChanged, createUserWithEmailAndPassword, signOut } = window.firebase;

function signUp(email, password) {
    return createUserWithEmailAndPassword(auth, email, password)
}

function signIn(email, password) {
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