/**
 * NGBC Session-Based Access Middleware
 *
 * Protects /NGBC/* and /api/ngbc/* routes with secure session-cookie auth.
 * The password is stored as NGBC_ACCESS_PASSWORD in Cloudflare Secrets.
 * Sessions are cryptographically random UUIDs stored in Cloudflare KV.
 *
 * Cookie settings:
 *   HttpOnly + Secure + SameSite=Strict + Path=/
 *
 * Session TTL: 8 hours
 */

const SESSION_TTL_SECONDS = 60 * 60 * 8; // 8 hours

// Path patterns that require authentication
const PROTECTED_PREFIXES = ["/NGBC/", "/api/ngbc/"];
const PROTECTED_EXACT = ["/NGBC"];
// GET /api/ngbc/capital-readiness is also protected (same as /api/capital-readiness)
const ADDITIONAL_PROTECTED = ["/api/capital-readiness"];

function isProtectedPath(pathname) {
  if (PROTECTED_EXACT.includes(pathname)) return true;
  if (PROTECTED_PREFIXES.some(prefix => pathname.startsWith(prefix))) return true;
  if (ADDITIONAL_PROTECTED.includes(pathname)) return true;
  return false;
}

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const pathname = url.pathname;

  // Allow CORS preflight and login/logout to pass through
  if (context.request.method === "OPTIONS") {
    return context.next();
  }

  if (!isProtectedPath(pathname)) {
    return context.next();
  }

  // Validate session from cookie
  const cookieHeader = context.request.headers.get("Cookie") || "";
  const sessionToken = parseSessionCookie(cookieHeader);

  if (!sessionToken) {
    return redirectToLogin(url);
  }

  // Look up session in KV
  let sessionData = null;
  try {
    if (context.env.NGBC_SESSIONS) {
      const raw = await context.env.NGBC_SESSIONS.get(sessionToken);
      if (raw) {
        sessionData = JSON.parse(raw);
      }
    }
  } catch {
    // KV read failed; treat as no session
  }

  if (!sessionData) {
    return redirectToLogin(url, "expired");
  }

  // Verify expiration
  const now = Date.now();
  if (now - sessionData.created > SESSION_TTL_SECONDS * 1000) {
    // Expired: delete and redirect
    try {
      if (context.env.NGBC_SESSIONS) {
        await context.env.NGBC_SESSIONS.delete(sessionToken);
      }
    } catch {
      // Best-effort deletion
    }
    return redirectToLogin(url, "expired");
  }

  // Authenticated — pass through to the requested resource
  const response = await context.next();

  // Add security headers to the response
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

function parseSessionCookie(cookieHeader) {
  const match = cookieHeader.match(/(?:^|;\s*)ngbc_session=([^;]*)/);
  return match ? match[1] : null;
}

function redirectToLogin(currentUrl, reason = "") {
  const loginUrl = new URL("/NGBC/login", currentUrl.origin);
  if (reason) {
    loginUrl.searchParams.set("reason", reason);
  }
  return new Response(null, {
    status: 302,
    headers: {
      Location: loginUrl.toString(),
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}
