const WebSocket = require('ws');
const CDP_HOST = 'localhost';
const CDP_PORT = 9522;
const TARGET_ID = 'D72FC6FE586092C1931250FB7935B285';
const WS_URL = `ws://${CDP_HOST}:${CDP_PORT}/devtools/page/${TARGET_ID}`;

let ws = null;
let msgId = 0;
const pending = {};

function connect() {
    return new Promise((resolve, reject) => {
        ws = new WebSocket(WS_URL);
        ws.on('open', resolve);
        ws.on('error', reject);
        ws.on('message', (data) => {
            const msg = JSON.parse(data);
            if (msg.id && pending[msg.id]) {
                pending[msg.id](msg);
                delete pending[msg.id];
            }
        });
    });
}

function send(method, params = {}, timeout = 25000) {
    return new Promise((resolve, reject) => {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            reject(new Error('WS not connected'));
            return;
        }
        const id = ++msgId;
        ws.send(JSON.stringify({ id, method, params }));
        const t = setTimeout(() => {
            delete pending[id];
            reject(new Error(`CDP timeout: ${method}`));
        }, timeout);
        pending[id] = (result) => {
            clearTimeout(t);
            resolve(result);
        };
    });
}

async function waitForStore(maxWait = 10000) {
    const start = Date.now();
    while (Date.now() - start < maxWait) {
        const r = await send('Runtime.evaluate', {
            expression: `window.store?.getState?.()?.globalSearch?.searchResults?.length || 0`,
            returnByValue: true,
            awaitPromise: false
        });
        const count = parseInt(r?.result?.value || r?.value || 0);
        if (count > 0) return count;
        await new Promise(r => setTimeout(r, 1000));
    }
    return 0;
}

async function main() {
    await connect();
    console.error('Connected, navigating...');

    await send('Page.navigate', { url: 'https://app.hoovers.dnb.com/search/company' });
    console.error('Waiting for page to load...');
    await new Promise(r => setTimeout(r, 5000)); // Wait for React to fully load

    // Check if input exists
    const inputCheck = await send('Runtime.evaluate', {
        expression: `document.querySelector('input.ant-input-lg')?.className || 'not found'`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Input class:', JSON.stringify(inputCheck));

    // Type
    console.error('Typing...');
    await send('Runtime.evaluate', {
        expression: `(function() {
            var input = document.querySelector('input.ant-input-lg');
            if (!input) return 'no input found';
            var ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            ns.call(input, 'Google LLC');
            input.dispatchEvent(new Event('input', {bubbles:true}));
            return 'typed: ' + input.value;
        })()`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Typed, waiting for Redux...');

    // Wait for Redux
    const count = await waitForStore(10000);
    console.error(`Redux results count: ${count}`);

    if (count > 0) {
        const results = await send('Runtime.evaluate', {
            expression: `JSON.stringify(window.store.getState().globalSearch.searchResults.slice(0,3).map(r => ({id: r.id, name: r.companyName})))`,
            returnByValue: true,
            awaitPromise: false
        });
        console.error('Results:', JSON.stringify(results));

        // Now click first result
        const firstResult = await send('Runtime.evaluate', {
            expression: `(function() {
                var results = window.store.getState().globalSearch.searchResults;
                if (!results || !results[0]) return 'no results';
                var id = results[0].id;
                // Try clicking on a link with this ID
                var links = Array.from(document.querySelectorAll('a'));
                var link = links.find(a => a.getAttribute('data-id') === id || a.href.includes(id));
                if (link) {
                    link.click();
                    return 'clicked: ' + link.href;
                }
                // Try finding by text
                var el = Array.from(document.querySelectorAll('*')).find(e => e.getAttribute('data-id') === id);
                if (el) {
                    el.click();
                    return 'clicked element with data-id: ' + id;
                }
                return 'could not find link for: ' + id;
            })()`,
            returnByValue: true,
            awaitPromise: false
        });
        console.error('Click result:', JSON.stringify(firstResult));

        await new Promise(r => setTimeout(r, 5000));
        const finalUrl = await send('Runtime.evaluate', {
            expression: `window.location.href + ' | ' + document.title`,
            returnByValue: true,
            awaitPromise: false
        });
        console.error('Final URL:', JSON.stringify(finalUrl));
    }

    ws.close();
}

main().catch(e => { console.error('ERROR:', e.message); if (ws) ws.close(); process.exit(1); });
