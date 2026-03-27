// firebase-config.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

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
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
