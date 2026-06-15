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

async function main() {
    await connect();

    // First do a fresh navigation to search
    await send('Page.navigate', { url: 'https://app.hoovers.dnb.com/search/company' });
    await new Promise(r => setTimeout(r, 4000));

    // Search
    await send('Runtime.evaluate', {
        expression: `(function() {
            var input = document.querySelector('input.ant-input-lg');
            if (!input) return 'no input';
            var ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            ns.call(input, 'Google LLC');
            input.dispatchEvent(new Event('input', {bubbles:true}));
            return 'typed';
        })()`,
        returnByValue: true,
        awaitPromise: false
    });
    await new Promise(r => setTimeout(r, 2500));

    // Get results
    const idsResult = await send('Runtime.evaluate', {
        expression: `JSON.stringify(window.store.getState().globalSearch.searchResults.slice(0,1).map(r => ({id: r.id, name: r.companyName})))`,
        returnByValue: true,
        awaitPromise: false
    });
    const results = JSON.parse(idsResult.result?.value || idsResult.value || '[]');
    console.error('Results:', JSON.stringify(results));

    if (results.length === 0) {
        // Try clearing and re-searching
        await send('Runtime.evaluate', {
            expression: `(function() {
                var input = document.querySelector('input.ant-input-lg');
                if (!input) return 'no input';
                input.value = '';
                input.dispatchEvent(new Event('input', {bubbles:true}));
                return 'cleared';
            })()`,
            returnByValue: true,
            awaitPromise: false
        });
        await new Promise(r => setTimeout(r, 1000));

        await send('Runtime.evaluate', {
            expression: `(function() {
                var input = document.querySelector('input.ant-input-lg');
                if (!input) return 'no input';
                var ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                ns.call(input, 'Apple Inc');
                input.dispatchEvent(new Event('input', {bubbles:true}));
                return 'typed: ' + input.value;
            })()`,
            returnByValue: true,
            awaitPromise: false
        });
        await new Promise(r => setTimeout(r, 2500));

        const idsResult2 = await send('Runtime.evaluate', {
            expression: `JSON.stringify(window.store.getState().globalSearch.searchResults.slice(0,3).map(r => ({id: r.id, name: r.companyName})))`,
            returnByValue: true,
            awaitPromise: false
        });
        console.error('Results after retry:', JSON.stringify(idsResult2));
    }

    ws.close();
}

main().catch(e => { console.error('ERROR:', e.message); if (ws) ws.close(); process.exit(1); });
