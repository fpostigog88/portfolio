/**
 * NGBC Login Handler
 * GET /NGBC/login — serves the login page
 * POST /NGBC/login — validates password and creates session
 */

const SESSION_COOKIE_NAME = "ngbc_session";
const SESSION_COOKIE_PATH = "/";
const SESSION_TTL_SECONDS = 60 * 60 * 8; // 8 hours
const MAX_LOGIN_BYTES = 200;

export async function onRequest(context) {
  if (context.request.method === "GET") {
    return serveLoginPage(context);
  }

  if (context.request.method === "POST") {
    return handleLoginAttempt(context);
  }

  return new Response("Method not allowed", { status: 405 });
}

async function serveLoginPage(context) {
  const url = new URL(context.request.url);
  const reason = url.searchParams.get("reason") || "";

  let expiredMessage = "";
  if (reason === "expired") {
    expiredMessage = "Session expired. Please sign in again.";
  } else if (reason === "logout") {
    expiredMessage = "You have been signed out.";
  }

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign in | NGBC Capital Readiness</title>
  <meta name="robots" content="noindex, nofollow, noarchive">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      background: #faf9f7;
      font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #1a1a2e;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }

    .login-card {
      width: 100%;
      max-width: 420px;
      background: #ffffff;
      border: 1px solid #e4dfd7;
      border-radius: 20px;
      box-shadow: 0 18px 50px rgba(31, 28, 23, 0.08);
      padding: 40px 36px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 32px;
      text-decoration: none;
      color: #1a1a2e;
    }

    .brand-mark {
      width: 34px;
      height: 34px;
      border-radius: 9px;
      background: #1a1a2e;
      color: #fff;
      display: grid;
      place-items: center;
      font-family: "Space Grotesk", sans-serif;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.04em;
    }

    .brand-name {
      font-family: "Space Grotesk", sans-serif;
      font-weight: 700;
      font-size: 1rem;
    }

    h1 {
      font-family: "Space Grotesk", sans-serif;
      font-size: 1.5rem;
      letter-spacing: -0.03em;
      margin: 0 0 6px;
    }

    .subtitle {
      color: #595866;
      font-size: 0.9rem;
      margin: 0 0 28px;
    }

    .expired-notice {
      background: #f4f1ec;
      border: 1px solid #cdc4b8;
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 0.85rem;
      color: #595866;
      margin-bottom: 20px;
    }

    label {
      display: block;
      font-size: 0.78rem;
      font-weight: 700;
      color: #595866;
      margin-bottom: 7px;
    }

    input[type="password"] {
      width: 100%;
      border: 1px solid #e4dfd7;
      border-radius: 10px;
      background: #fff;
      color: #1a1a2e;
      font: inherit;
      font-size: 1rem;
      padding: 12px 13px;
      outline: none;
      transition: border-color 160ms ease, box-shadow 160ms ease;
    }

    input[type="password"]:focus {
      border-color: #b8956a;
      box-shadow: 0 0 0 3px rgba(184, 149, 106, 0.14);
    }

    .submit-btn {
      width: 100%;
      min-height: 48px;
      border: 1px solid #1a1a2e;
      border-radius: 10px;
      background: #1a1a2e;
      color: #fff;
      font: inherit;
      font-size: 0.95rem;
      font-weight: 800;
      cursor: pointer;
      margin-top: 20px;
      transition: background 160ms ease;
    }

    .submit-btn:hover { background: #2a2942; }
    .submit-btn:disabled { opacity: 0.6; cursor: wait; }

    .error-msg {
      background: #fff8f8;
      border: 1px solid #fecaca;
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 0.85rem;
      color: #b42318;
      margin-bottom: 16px;
      display: none;
    }

    .error-msg.visible { display: block; }

    .back-link {
      display: block;
      text-align: center;
      margin-top: 20px;
      color: #85828d;
      font-size: 0.82rem;
      text-decoration: none;
    }

    .back-link:hover { color: #595866; }
  </style>
</head>
<body>
  <div class="login-card">
    <a class="brand" href="/">
      <span class="brand-mark">FP</span>
      <span class="brand-name">Felipe Postigo</span>
    </a>

    <h1>Sign in</h1>
    <p class="subtitle">NGBC Capital Readiness Agent</p>

    ${expiredMessage ? `<div class="expired-notice">${escapeHtml(expiredMessage)}</div>` : ""}

    <div id="error-box" class="error-msg" role="alert"></div>

    <form id="login-form" method="POST" action="/NGBC/login" novalidate>
      <label for="password">Password</label>
      <input
        id="password"
        name="password"
        type="password"
        autocomplete="current-password"
        placeholder="Enter access password"
        maxlength="128"
        required
        autofocus
      >
      <button class="submit-btn" type="submit" id="submit-btn">Sign in</button>
    </form>

    <a class="back-link" href="/">Back to portfolio</a>
  </div>

  <script>
    const form = document.getElementById("login-form");
    const errorBox = document.getElementById("error-box");
    const submitBtn = document.getElementById("submit-btn");

    form.addEventListener("submit", () => {
      submitBtn.disabled = true;
      submitBtn.textContent = "Signing in…";
    });
  </script>
</body>
</html>`;

  return new Response(html, {
    status: 200,
    headers: {
      "Content-Type": "text/html; charset=UTF-8",
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}

async function handleLoginAttempt(context) {
  let password = "";
  let contentLength = 0;

  try {
    contentLength = Number(context.request.headers.get("Content-Length") || 0);
    if (contentLength > MAX_LOGIN_BYTES) {
      return jsonError("Request too large.", 400);
    }
    const rawBody = await context.request.text();
    const params = new URLSearchParams(rawBody);
    password = params.get("password") || "";
  } catch {
    return jsonError("Invalid request.", 400);
  }

  if (!password) {
    return jsonError("Password is required.", 401);
  }

  // Retrieve the stored password from Cloudflare Secrets
  const storedPassword = context.env.NGBC_ACCESS_PASSWORD || "";
  if (!storedPassword) {
    console.error("NGBC_ACCESS_PASSWORD secret is not configured");
    return jsonError("Access not configured.", 500);
  }

  // Constant-time comparison to prevent timing attacks
  let matched = false;
  if (password.length === storedPassword.length) {
    let diff = 0;
    for (let i = 0; i < password.length; i++) {
      diff |= password.charCodeAt(i) ^ storedPassword.charCodeAt(i);
    }
    matched = diff === 0;
  }

  if (!matched) {
    // Small delay to deter brute-force even on wrong passwords
    await new Promise(resolve => setTimeout(resolve, 300));
    return jsonError("Incorrect password.", 401);
  }

  // Generate a cryptographically random session token
  const sessionToken = crypto.randomUUID();

  // Store session in KV with TTL
  const sessionData = JSON.stringify({
    created: Date.now(),
    ua: context.request.headers.get("User-Agent") || ""
  });

  try {
    if (context.env.NGBC_SESSIONS) {
      await context.env.NGBC_SESSIONS.put(sessionToken, sessionData, {
        expirationTtl: SESSION_TTL_SECONDS
      });
    }
  } catch (err) {
    console.error("KV session write failed:", err);
    return jsonError("Could not create session.", 500);
  }

  // Redirect to /NGBC after successful login
  const redirectUrl = new URL("/NGBC", context.request.url).toString();

  return new Response(null, {
    status: 302,
    headers: {
      Location: redirectUrl,
      "Set-Cookie":
        `${SESSION_COOKIE_NAME}=${sessionToken}; ` +
        `Path=${SESSION_COOKIE_PATH}; ` +
        `HttpOnly; ` +
        `Secure; ` +
        `SameSite=Strict; ` +
        `Max-Age=${SESSION_TTL_SECONDS}`,
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}

function jsonError(message, status) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
