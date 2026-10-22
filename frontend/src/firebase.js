import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBKCC58uZh8w5GCcdlSjOCbnA_O5ShMXkk",
  authDomain: "uluk-ata-442fd.firebaseapp.com",
  projectId: "uluk-ata-442fd",
  storageBucket: "uluk-ata-442fd.firebasestorage.app",
  messagingSenderId: "798416768572",
  appId: "1:798416768572:web:d80c3b17b470de2ae0fd39",
  measurementId: "G-GN24VNP3NW"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
