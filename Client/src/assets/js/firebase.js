const { initializeApp, getAnalytics, getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } = window.firebase;
const firebaseConfig = {
  apiKey: "AIzaSyB2hqbLL4oq5DhGOH4plB8YJ7IxzPioKrA",
  authDomain: "flightbot-5f664.firebaseapp.com",
  projectId: "flightbot-5f664",
  storageBucket: "flightbot-5f664.appspot.com",
  messagingSenderId: "882657740955",
  appId: "1:882657740955:web:fcaeedebd06e9dc4bc1e3e",
  measurementId: "G-EX1N0GHY1K"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const auth = getAuth();
export default app;
export { auth };