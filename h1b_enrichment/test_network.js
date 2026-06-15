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
    console.error('Connected');

    // First, search and get a company ID
    await send('Page.navigate', { url: 'https://app.hoovers.dnb.com/search/company' });
    await new Promise(r => setTimeout(r, 4000));

    // Search for Google
    const typeResult = await send('Runtime.evaluate', {
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
    console.error('Type:', JSON.stringify(typeResult));
    await new Promise(r => setTimeout(r, 2000));

    // Get company IDs from Redux
    const idsResult = await send('Runtime.evaluate', {
        expression: `JSON.stringify(window.store.getState().globalSearch.searchResults.slice(0,1).map(r => ({id: r.id, name: r.companyName})))`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('IDs:', JSON.stringify(idsResult));

    const firstId = JSON.parse(idsResult.result?.value || idsResult.value || '[]')[0]?.id;
    if (!firstId) { console.error('No results'); process.exit(1); }

    // Enable network monitoring
    await send('Network.enable');
    await send('Page.enable');

    // Track requests
    const apiCalls = [];
    const origSend = ws.send.bind(ws);
    ws.send = (data) => {
        const parsed = JSON.parse(data);
        if (parsed.method && parsed.method.startsWith('Network')) {
            apiCalls.push({ method: parsed.method, params: parsed.params });
        }
        return origSend(data);
    };

    // Navigate to company profile using the ID
    console.error('Navigating to company profile...');
    await send('Page.navigate', { url: `https://app.hoovers.dnb.com/company/${firstId}` });
    await new Promise(r => setTimeout(r, 5000));

    const urlResult = await send('Runtime.evaluate', {
        expression: `window.location.href`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Final URL:', JSON.stringify(urlResult));

    // Check if we're on the profile page
    const titleResult = await send('Runtime.evaluate', {
        expression: `document.title`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Title:', JSON.stringify(titleResult));

    // Check Redux company state
    const companyKeys = await send('Runtime.evaluate', {
        expression: `JSON.stringify(Object.keys(window.store.getState().company || {}).slice(0, 15))`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Company state keys:', JSON.stringify(companyKeys));

    // Check companyData
    const companyDataCheck = await send('Runtime.evaluate', {
        expression: `(function() {
            var c = window.store.getState().company;
            return JSON.stringify({
                hasData: !!(c && Object.keys(c).length > 0),
                count: c ? Object.keys(c).length : 0,
                primitive: c?.primitive ? 'yes' : 'no',
                gridConfigs: c?.gridConfigs ? 'yes' : 'no'
            });
        })()`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Company data check:', JSON.stringify(companyDataCheck));

    // Check if there's a companyDetail or companyInfo in the state
    const stateCheck = await send('Runtime.evaluate', {
        expression: `(function() {
            var state = window.store.getState();
            var keys = Object.keys(state).filter(k => k.toLowerCase().includes('company') || k.toLowerCase().includes('contact') || k.toLowerCase().includes('executive'));
            return JSON.stringify(keys);
        })()`,
        returnByValue: true,
        awaitPromise: false
    });
    console.error('Relevant state keys:', JSON.stringify(stateCheck));

    ws.close();
}

main().catch(e => { console.error('ERROR:', e.message); if (ws) ws.close(); process.exit(1); });
