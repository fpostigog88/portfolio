/**
 * Hoovers CDP - Company Search via Chrome Redux
 * ==========================================
 * Uses Chrome CDP + React synthetic events + Redux state extraction.
 * 
 * Key discovery: The search input's onChange updates Redux globalSearch.searchResults[]
 * Data available: companyName, numEmployees, salesUsd, addresses[], id
 * 
 * Usage:
 *   node hoovers_cdp.js search "Apple Inc"
 *   node hoovers_cdp.js batch companies.txt
 */

const WebSocket = require('ws');
const FS = require('fs');

const CDP_HOST = 'localhost';
const CDP_PORT = 9522;
const TARGET_ID = 'D72FC6FE586092C1931250FB7935B285';
const WS_URL = `ws://${CDP_HOST}:${CDP_PORT}/devtools/page/${TARGET_ID}`;

let ws = null;
let msgId = 0;
const pending = {};

function send(method, params = {}) {
    return new Promise((resolve, reject) => {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            reject(new Error('Not connected')); return;
        }
        const id = ++msgId;
        ws.send(JSON.stringify({ id, method, params }));
        const timeout = setTimeout(() => {
            if (pending[id]) { delete pending[id]; reject(new Error('CDP timeout')); }
        }, 20000);
        pending[id] = (result) => {
            clearTimeout(timeout); delete pending[id];
            if (result.error) reject(new Error(result.error.message || result.error));
            else resolve(result.result || result);
        };
    });
}

async function connect() {
    return new Promise((resolve, reject) => {
        ws = new WebSocket(WS_URL);
        ws.on('open', resolve);
        ws.on('error', reject);
        ws.on('message', (data) => {
            const msg = JSON.parse(data);
            if (msg.id && pending[msg.id]) pending[msg.id](msg);
        });
    });
}

async function navigate(url) {
    await send('Page.navigate', { url });
    await new Promise(r => setTimeout(r, 2500));
}

async function evalJs(js) {
    const result = await send('Runtime.evaluate', {
        expression: js,
        returnByValue: true,
        awaitPromise: false
    });
    if (result.exceptionDetails) {
        return { error: result.exceptionDetails.exceptionDescription };
    }
    return result.result?.value ?? result.value ?? '';
}

function formatCurrency(amount) {
    if (!amount) return '';
    try {
        amount = parseFloat(amount);
        if (amount >= 1e9) return '$' + (amount / 1e9).toFixed(2) + 'B';
        if (amount >= 1e6) return '$' + (amount / 1e6).toFixed(2) + 'M';
        return '$' + amount.toLocaleString();
    } catch(e) { return String(amount); }
}

async function searchCompany(name, maxResults = 5) {
    // Navigate to search
    await navigate('https://app.hoovers.dnb.com/search/company');

    // Type using React synthetic event
    const escaped = name.replace(/'/g, "\'");
    await evalJs(`
        (function() {
            var input = document.querySelector('input.ant-input-lg');
            if (!input) return 'not found';
            var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeSetter.call(input, '${escaped}');
            input.dispatchEvent(new Event('input', { bubbles: true }));
            return 'typed: ' + input.value;
        })()
    `);

    await new Promise(r => setTimeout(r, 2000));

    // Extract from Redux
    const dataStr = await evalJs(`
        (function() {
            var state = window.store.getState();
            var gs = state.globalSearch;
            var results = gs.searchResults || [];
            return JSON.stringify({
                count: results.length,
                companies: results.map(function(r) {
                    return {
                        companyName: r.companyName || '',
                        numEmployees: r.numEmployees || 0,
                        salesUsd: r.salesUsd || 0,
                        city: r.addresses && r.addresses[0] ? (r.addresses[0].city || '') : '',
                        stateName: r.addresses && r.addresses[0] && r.addresses[0].stateOrProvince ? (r.addresses[0].stateOrProvince.name || '') : '',
                        countryName: r.addresses && r.addresses[0] && r.addresses[0].country ? (r.addresses[0].country.name || '') : '',
                        id: r.id || ''
                    };
                }).slice(0, ${maxResults})
            });
        })()
    `);

    try {
        return JSON.parse(dataStr);
    } catch(e) {
        return { count: 0, companies: [], error: e.message };
    }
}

async function cmdSearch(query) {
    await connect();
    console.error('Searching:', query);

    const data = await searchCompany(query, 10);
    console.error('Found', data.count || 0, 'results\n');

    for (const c of (data.companies || [])) {
        console.log(JSON.stringify({
            companyName: c.companyName,
            employees: c.numEmployees,
            revenue: formatCurrency(c.salesUsd),
            revenue_usd: c.salesUsd,
            city: c.city,
            state: c.stateName,
            country: c.countryName,
            hoovers_id: c.id
        }));
    }

    ws.close();
}

async function cmdBatch(file) {
    const companies = FS.readFileSync(file, 'utf-8')
        .split('\n')
        .map(l => l.trim())
        .filter(l => l && !l.startsWith('#'));

    console.error(`Batch enrichment: ${companies.length} companies`);

    await connect();

    const results = [];
    for (let i = 0; i < Math.min(companies.length, 500); i++) {
        console.error(`[${i+1}/${Math.min(companies.length, 500)}] ${companies[i]}...`);
        const data = await searchCompany(companies[i], 1);

        if (data.companies && data.companies.length > 0) {
            const c = data.companies[0];
            const enriched = {
                source_name: companies[i],
                matched_name: c.companyName,
                employees: c.numEmployees,
                revenue: formatCurrency(c.salesUsd),
                revenue_usd: c.salesUsd,
                city: c.city,
                state: c.stateName,
                country: c.countryName,
                hoovers_id: c.id
            };
            results.push(enriched);
            console.error(`  -> ${c.companyName} | ${c.numEmployees} employees | ${formatCurrency(c.salesUsd)}`);
        } else {
            results.push({ source_name: companies[i], error: 'not found' });
            console.error(`  -> NOT FOUND`);
        }

        await new Promise(r => setTimeout(r, 1500));
    }

    const output = file.replace('.txt', '_enriched.json');
    FS.writeFileSync(output, JSON.stringify(results, null, 2));
    console.error(`\nSaved ${results.length} results to: ${output}`);

    ws.close();
}

async function cmdTest() {
    await connect();
    console.error('Testing with Apple...');
    const data = await searchCompany('Apple', 3);
    console.error('\nResults:');
    for (const c of (data.companies || [])) {
        console.error(`  ${c.companyName} | ${c.numEmployees} employees | ${formatCurrency(c.salesUsd)} | ${c.city}, ${c.stateName}`);
    }
    ws.close();
}

// Entry point
const [,, cmd, ...args] = process.argv;

const commands = {
    test: cmdTest,
    search: () => cmdSearch(args.join(' ')),
    batch: () => cmdBatch(args[0]),
};

if (commands[cmd]) {
    commands[cmd]().catch(e => {
        console.error('Error:', e.message);
        if (ws) ws.close();
        process.exit(1);
    });
} else {
    console.log('Usage: node hoovers_cdp.js test|search|batch');
    console.log('  test             - test with Apple');
    console.log('  search "Apple"   - search for a company');
    console.log('  batch list.txt   - batch enrich from file');
}
