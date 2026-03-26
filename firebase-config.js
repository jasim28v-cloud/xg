import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-app.js";
import { getDatabase } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-database.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-auth.js";
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.7.2/firebase-storage.js";

const firebaseConfig = {
  apiKey: "AIzaSyBMKBnXRZ2mL5C2FYRih6NSpBIbebYeTBI",
  authDomain: "porn-dc411.firebaseapp.com",
  databaseURL: "https://porn-dc411-default-rtdb.firebaseio.com",
  projectId: "porn-dc411",
  storageBucket: "porn-dc411.firebasestorage.app",
  messagingSenderId: "344117985586",
  appId: "1:344117985586:web:d1064a4fd269983174572b",
  measurementId: "G-CZ6E0V68WZ"
};

const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
const auth = getAuth(app);
const storage = getStorage(app);

export { database, auth, storage, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut, onAuthStateChanged, storageRef, uploadBytes, getDownloadURL };
