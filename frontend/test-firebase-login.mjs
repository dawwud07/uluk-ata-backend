import { login } from "./src/auth.js";

const email = process.argv[2];
const password = process.argv[3];
if (!email || !password) {
  console.error("Usage: node test-firebase-login.mjs <email> <password>");
  process.exit(1);
}

const BASE = process.env.BACKEND_URL || "http://127.0.0.1:8000";

try {
  const idToken = await login(email, password);
  console.log("TOKEN_OK prefix:", idToken.slice(0, 20));

  for (const path of ["/api/v1/users/profile/", "/api/v1/profile/orders/"]) {
    const res = await fetch(`${BASE}${path}`, {
      headers: { Authorization: `Bearer ${idToken}` },
    });
    const text = await res.text();
    console.log(path, "->", res.status, text.slice(0, 300));
  }
} catch (e) {
  console.error("LOGIN_FAILED:", e?.code || e?.message || e);
  process.exit(1);
}
