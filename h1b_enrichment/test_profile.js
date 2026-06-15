const { WebSocket } = require('ws');
const CDP_HOST = 'localhost';
const CDP_PORT = 9522;
const TARGET_ID = 'D72FC6FE586092C1931250FB7935B285';
const WS_URL = `ws://${CDP_HOST}:${CDP_PORT}/devtools/page/${TARGET_ID}`;

function cdp(method, params = {}) {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket(WS_URL);
        let timeout = setTimeout(() => { try { ws.close(); } catch(e) {} reject(new Error('CDP timeout')); }, 25000);
        ws.on('open', () => {
            const id = Date.now();
            ws.send(JSON.stringify({ id, method, params }));
            ws.on('message', (data) => {
                const msg = JSON.parse(data);
                if (msg.id === id) { clearTimeout(timeout); ws.close(); resolve(msg.result || msg); }
            });
        });
        ws.on('error', (e) => { clearTimeout(timeout); try { ws.close(); } catch(e) {} reject(e); });
    });
}

async function main() {
    // Search for Apple
    const typeResult = await cdp('Runtime.evaluate', {
        expression: `(function() {
            var input = document.querySelector('input.ant-input-lg');
            if (!input) return 'no input';
            var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeSetter.call(input, 'Apple Inc');
            input.dispatchEvent(new Event('input', { bubbles: true }));
            return 'typed';
        })()`,
        returnByValue: true
    });
    console.error('Type result:', JSON.stringify(typeResult));
    await new Promise(r => setTimeout(r, 2000));

    // Get company links from page
    const linksResult = await cdp('Runtime.evaluate', {
        expression: `JSON.stringify(Array.from(document.querySelectorAll('a[href*="/company/"]')).slice(0,5).map(a => ({href: a.href, text: a.textContent.trim().substring(0,50)})))`,
        returnByValue: true
    });
    console.error('Links:', JSON.stringify(linksResult));

    // Get IDs from Redux
    const idsResult = await cdp('Runtime.evaluate', {
        expression: `JSON.stringify(window.store.getState().globalSearch.searchResults.slice(0,3).map(r => r.id))`,
        returnByValue: true
    });
    console.error('Redux IDs:', JSON.stringify(idsResult));
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
