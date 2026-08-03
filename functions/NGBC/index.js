/**
 * NGBC Index Handler
 * Serves protected NGBC static assets from _assets/ngbc/
 * Auth is enforced by _middleware.js before this handler is reached.
 */
export async function onRequest(context) {
  const url = new URL(context.request.url);
  let filePath;

  if (url.pathname === "/NGBC" || url.pathname === "/NGBC/") {
    filePath = "/_assets/ngbc/index.html";
  } else if (url.pathname.startsWith("/NGBC/")) {
    // Strip /NGBC prefix and serve from _assets/ngbc/
    const remainder = url.pathname.slice("/NGBC".length);
    filePath = `/_assets/ngbc${remainder}`;
  }

  const assetUrl = new URL(filePath, context.request.url);
  const assetResponse = await fetch(assetUrl.toString());

  if (!assetResponse.ok) {
    return new Response("Not found", {
      status: 404,
      headers: {
        "Content-Type": "text/plain",
        "Cache-Control": "private, no-store",
        "X-Robots-Tag": "noindex, nofollow, noarchive"
      }
    });
  }

  const contentType = filePath.endsWith(".html")
    ? "text/html; charset=utf-8"
    : filePath.endsWith(".css")
    ? "text/css"
    : filePath.endsWith(".js")
    ? "application/javascript"
    : "text/plain";

  return new Response(assetResponse.body, {
    status: 200,
    headers: {
      "Content-Type": contentType,
      "Cache-Control": "private, no-store",
      "X-Robots-Tag": "noindex, nofollow, noarchive"
    }
  });
}
