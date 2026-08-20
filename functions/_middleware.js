/**
 * NGBC Session-Based Access Middleware
 * Uses signed HMAC-SHA256 session tokens (stateless, no KV needed).
 * Password stored as NGBC_ACCESS_PASSWORD in Cloudflare Secrets.
 *
 * Cookie: HttpOnly + Secure + SameSite=Strict + Path=/
 * Session TTL: 8 hours
 */

const SESSION_TTL_MS = 60 * 60 * 8 * 1000; // 8 hours
const COOKIE_NAME = "ngbc_session";

const PROTECTED_PREFIXES = ["/NGBC/", "/api/ngbc/"];
const PROTECTED_EXACT = ["/NGBC"];
const ADDITIONAL_PROTECTED = ["/api/capital-readiness"];
const PUBLIC_PATHS = ["/NGBC/login", "/NGBC/logout"];

function isProtectedPath(pathname) {
  if (PROTECTED_EXACT.includes(pathname)) return true;
  if (PROTECTED_PREFIXES.some(p => pathname.startsWith(p))) return true;
  if (ADDITIONAL_PROTECTED.includes(pathname)) return true;
  return false;
}

function isPublicPath(pathname) {
  return PUBLIC_PATHS.includes(pathname);
}

function base64UrlEncode(buffer) {
  const bytes = buffer instanceof Uint8Array ? buffer : new TextEncoder().encode(buffer);
  let binary = "";
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=/g, "");
}

function base64UrlDecode(str) {
  str = str.replace(/-/g, "+").replace(/_/g, "/");
  while (str.length % 4) str += "=";
  const binary = atob(str);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

function createSignature(secret, headerB64, payloadB64) {
  const data = new TextEncoder().encode(`${headerB64}.${payloadB64}`);
  const key = crypto.createSecretKey(base64UrlDecode(secret), "raw");
  return crypto.subtle.sign("HMAC", key, data).then(base64UrlEncode);
}

async function verifyToken(secret, token) {
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  const [headerB64, payloadB64, sigB64] = parts;

  // Verify signature
  const key = crypto.createSecretKey(base64UrlDecode(secret), "raw");
  const data = new TextEncoder().encode(`${headerB64}.${payloadB64}`);
  const valid = await crypto.subtle.verify("HMAC", key, base64UrlDecode(sigB64), data);
  if (!valid) return null;

  // Decode payload
  const payload = JSON.parse(new TextDecoder().decode(base64UrlDecode(payloadB64)));
  const now = Date.now();
  if (now - payload.created > SESSION_TTL_MS) return null; // expired
  return payload;
}

function parseSessionCookie(cookieHeader) {
  const match = (cookieHeader || "").match(new RegExp(`(?:^|;\\\\s*)${COOKIE_NAME}=([^;]*)`));
  return match ? match[1] : null;
}

function makeSessionCookie(token, maxAge) {
  const expires = new Date(Date.now() + maxAge).toUTCString();
  return `${COOKIE_NAME}=${token}; Path=/; HttpOnly; Secure; SameSite=Strict; Expires=${expires}`;
}

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const pathname = url.pathname;

  if (context.request.method === "OPTIONS" || isPublicPath(pathname)) {
    return context.next();
  }

  if (!isProtectedPath(pathname)) {
    return context.next();
  }

  const secret = context.env.NGBC_ACCESS_PASSWORD || "";
  const cookieHeader = context.request.headers.get("Cookie") || "";
  const token = parseSessionCookie(cookieHeader);

  if (!token) {
    return redirectToLogin(url);
  }

  const payload = await verifyToken(secret, token).catch(() => null);
  if (!payload) {
    return redirectToLogin(url, payload === null ? "invalid" : "expired");
  }

  // Authenticated — pass through
  const response = await context.next();

  const headers = new Headers(response.headers);
  headers.set("Cache-Control", "private, no-store");
  headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("Referrer-Policy", "no-referrer");

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}

function redirectToLogin(currentUrl, reason = "") {
  const loginUrl = new URL("/NGBC/login", currentUrl.origin);
  if (reason) loginUrl.searchParams.set("reason", reason);
  return new Response(null, {
    status: 302,
    headers: {
      Location: loginUrl.toString(),
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}
