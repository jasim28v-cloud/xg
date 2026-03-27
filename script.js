import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.0/firebase-auth.js";
import { getDatabase, ref, push, set, onValue, update, get, child } from "https://www.gstatic.com/firebasejs/10.7.0/firebase-database.js";

const firebaseConfig = {
    apiKey: "AIzaSyBMKBnXRZ2mL5C2FYRih6NSpBIbebYeTBI",
    authDomain: "porn-dc411.firebaseapp.com",
    databaseURL: "https://porn-dc411-default-rtdb.firebaseio.com",
    projectId: "porn-dc411",
    storageBucket: "porn-dc411.firebasestorage.app",
    messagingSenderId: "344117985586",
    appId: "1:344117985586:web:d1064a4fd269983174572b"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getDatabase(app);

export { ref, push, set, onValue, update, get, child };

// Cloudinary Configuration
export const CLOUD_NAME = 'dnillsbmi';
export const UPLOAD_PRESET = 'ekxzvogb';
