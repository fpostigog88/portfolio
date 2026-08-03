/**
 * NGBC Logout Handler
 * POST /NGBC/logout — destroys the session cookie
 */

const SESSION_COOKIE_NAME = "ngbc_session";

export async function onRequest(context) {
  if (context.request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const cookieHeader = context.request.headers.get("Cookie") || "";
  const sessionToken = parseSessionCookie(cookieHeader);

  // Best-effort session deletion from KV
  if (sessionToken && context.env.NGBC_SESSIONS) {
    try {
      await context.env.NGBC_SESSIONS.delete(sessionToken);
    } catch {
      // Continue regardless
    }
  }

  // Expire the cookie immediately
  const redirectUrl = new URL("/NGBC/login?reason=logout", context.request.url).toString();

  return new Response(null, {
    status: 302,
    headers: {
      Location: redirectUrl,
      "Set-Cookie":
        `${SESSION_COOKIE_NAME}=; ` +
        `Path=/; ` +
        `HttpOnly; ` +
        `Secure; ` +
        `SameSite=Strict; ` +
        `Max-Age=0`,
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}

function parseSessionCookie(cookieHeader) {
  const match = cookieHeader.match(/(?:^|;\s*)ngbc_session=([^;]*)/);
  return match ? match[1] : null;
}
