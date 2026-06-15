const WebSocket = require('ws');
const CDP_HOST = 'localhost';
const CDP_PORT = 9522;
const TARGET_ID = 'D72FC6FE586092C1931250FB7935B285';
const WS_URL = `ws://${CDP_HOST}:${CDP_PORT}/devtools/page/${TARGET_ID}`;

function cdp(method, params = {}) {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket(WS_URL);
        let t = setTimeout(() => { try { ws.close(); } catch(e) {} reject(new Error('timeout')); }, 20000);
        ws.on('open', () => {
            const id = Date.now();
            ws.send(JSON.stringify({ id, method, params }));
            ws.on('message', (data) => {
                const msg = JSON.parse(data);
                if (msg.id === id) { clearTimeout(t); ws.close(); resolve(msg.result || msg); }
            });
        });
        ws.on('error', (e) => { clearTimeout(t); try { ws.close(); } catch(e) {} reject(e); });
    });
}

async function main() {
    // Search
    await cdp('Runtime.evaluate', {
        expression: `(function() {
            var input = document.querySelector('input.ant-input-lg');
            if (!input) return 'no input';
            var ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            ns.call(input, 'Google LLC');
            input.dispatchEvent(new Event('input', {bubbles:true}));
            return 'typed';
        })()`,
        returnByValue: true
    });
    await new Promise(r => setTimeout(r, 2000));

    // Get Redux IDs
    const ids = await cdp('Runtime.evaluate', {
        expression: `JSON.stringify(window.store.getState().globalSearch.searchResults.slice(0,3).map(r => ({id: r.id, name: r.companyName})))`,
        returnByValue: true
    });
    console.error('IDs:', ids.result?.value || ids.value);

    // Try to get the first result ID and click its link
    const firstResult = await cdp('Runtime.evaluate', {
        expression: `(function() {
            var results = window.store.getState().globalSearch.searchResults;
            if (!results || !results[0]) return 'no results';
            var id = results[0].id;
            // Try clicking by data-id attribute
            var el = document.querySelector('[data-id="' + id + '"]');
            if (el) { el.click(); return 'clicked by data-id: ' + id; }
            // Try parent link
            var parent = el?.parentElement;
            if (parent && parent.href && parent.href.includes('company')) {
                parent.click(); return 'clicked parent: ' + parent.href;
            }
            return 'data-id not found for: ' + id;
        })()`,
        returnByValue: true
    });
    console.error('Click result:', firstResult.result?.value || firstResult.value);

    await new Promise(r => setTimeout(r, 4000));

    // Check URL
    const url = await cdp('Runtime.evaluate', {
        expression: `window.location.href + ' | ' + document.title`,
        returnByValue: true
    });
    console.error('URL:', url.result?.value || url.value);

    // Check company state
    const companyState = await cdp('Runtime.evaluate', {
        expression: `JSON.stringify(Object.keys(window.store.getState().company || {}).slice(0, 20))`,
        returnByValue: true
    });
    console.error('Company state keys:', companyState.result?.value || companyState.value);
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
