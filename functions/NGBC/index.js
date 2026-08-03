/**
 * NGBC Index Handler
 * Serves the static index.html from this directory after auth via middleware.
 * context.next() allows Cloudflare Pages to serve the adjacent index.html.
 */
export async function onRequest(context) {
  return context.next();
}
