/**
 * Hoovers Full Profile Scraper
 * Visits each company profile and extracts all available data:
 * - Company overview (employees, revenue, address, industry, description)
 * - Contact info (phone, fax, key contacts)
 * - Management structure (Executives)
 * - Financial data (revenue, employees, years in business)
 * - Stock info (ticker, exchange)
 * - Parent/subsidiary structure
 * - Competitors
 * - Industry classification
 * - And more from Redux store
 */

const WebSocket = require('ws');
const fs = require('fs');
const readline = require('readline');

const CDP_HOST = 'localhost';
const CDP_PORT = 9522;
const TARGET_ID = 'D72FC6FE586092C1931250FB7935B285';
const WS_URL = `ws://${CDP_HOST}:{CDP_PORT}/devtools/page/${TARGET_ID}`;

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
                const cb = pending[msg.id];
                delete pending[msg.id];
                cb(msg.result || msg);
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

async function navigate(url) {
    await send('Page.navigate', { url });
    await new Promise(r => setTimeout(r, 3500)); // Wait for React to render
}

async function evalJs(js) {
    const r = await send('Runtime.evaluate', {
        expression: js,
        returnByValue: true,
        awaitPromise: false
    });
    if (r.exceptionDetails) {
        return { error: r.exceptionDetails.exceptionDescription };
    }
    return r.result?.value ?? r.value ?? '';
}

async function getPageData() {
    // Extract everything from Redux store
    const data = await evalJs(`
        (function() {
            try {
                const state = window.store.getState();
                const c = state.company;

                // Company overview section
                const overview = {
                    id: c?.companyData?.id || c?.id || '',
                    legalName: c?.companyData?.legalName || c?.legalName || '',
                    shortName: c?.companyData?.shortName || c?.shortName || '',
                    description: c?.companyData?.description || c?.description || '',
                    website: c?.companyData?.website || c?.website || '',
                    yearFounded: c?.companyData?.yearFounded || c?.yearFounded || '',
                    ownershipType: c?.companyData?.ownershipType || c?.ownershipType || '',
                    employeeRange: c?.companyData?.employeeRange || c?.employeeRange || '',
                    revenueRange: c?.companyData?.revenueRange || c?.revenueRange || '',
                    numEmployees: c?.companyData?.numEmployees || c?.numEmployees || 0,
                    salesUsd: c?.companyData?.salesUsd || c?.salesUsd || 0,
                    ticker: c?.companyData?.stockExchangeTicker || c?.stockExchangeTicker || '',
                    stockExchange: c?.companyData?.stockExchange || c?.stockExchange || '',
                    duns: c?.companyData?.duns || c?.duns || '',
                    naics: c?.companyData?.naics5?.naicsCode || c?.naics5?.naicsCode || '',
                    naicsDesc: c?.companyData?.naics5?.naicsDescription || c?.naics5?.naicsDescription || '',
                    sic: c?.companyData?.sic4?.sicCode || c?.sic4?.sicCode || '',
                    sicDesc: c?.companyData?.sic4?.sicDescription || c?.sic4?.sicDescription || '',
                };

                // Address
                const addr = c?.companyData?.addresses?.[0] || c?.addresses?.[0] || {};
                overview.address = {
                    street: addr.streetAddress || '',
                    city: addr.city || '',
                    state: addr.stateOrProvince?.name || addr.stateOrProvinceName || '',
                    postalCode: addr.postalCode || '',
                    country: addr.country?.name || addr.countryName || ''
                };

                // Phone/fax from contact section
                const contact = {
                    phone: c?.companyData?.phoneNumber || c?.phoneNumber || '',
                    fax: c?.companyData?.faxNumber || c?.faxNumber || ''
                };

                // Key contacts
                const contacts = (c?.companyData?.keyContacts || c?.keyContacts || []).slice(0, 10).map(kc => ({
                    name: kc.name || '',
                    title: kc.jobTitle || kc.title || '',
                    department: kc.department || ''
                }));

                // Executives
                const execs = (c?.companyData?.executives || c?.executives || []).slice(0, 20).map(ex => ({
                    name: ex.name || '',
                    title: ex.jobTitle || ex.title || '',
                    isCeo: ex.isChiefExecutive || false
                }));

                // Parent/child relationships
                const corporateFamily = c?.companyData?.corporateFamily || c?.corporateFamily || {};
                const relationships = {
                    isSubsidiary: corporateFamily?.isSubsidiary || false,
                    parentName: corporateFamily?.parent?.legalName || corporateFamily?.parentName || '',
                    parentId: corporateFamily?.parent?.id || corporateFamily?.parentId || '',
                    hierarchyLevel: corporateFamily?.hierarchyLevel || '',
                    numberOfSubsidiaries: corporateFamily?.numberOfImmediateSubsidiaries || 0,
                    totalSubsidiaries: corporateFamily?.totalSubsidiaries || 0
                };

                // Financials
                const financials = {
                    revenue: c?.companyData?.salesUsd || c?.salesUsd || 0,
                    revenueRaw: c?.companyData?.salesUsd || c?.salesUsd || 0,
                    employees: c?.companyData?.numEmployees || c?.numEmployees || 0,
                    marketCap: c?.companyData?.marketCap || '',
                };

                // Competitors
                const competitors = (c?.companyData?.competitors || c?.competitors || []).slice(0, 10).map(comp => ({
                    name: comp.name || '',
                    id: comp.id || ''
                }));

                return JSON.stringify({
                    overview,
                    contact,
                    contacts,
                    executives: execs,
                    relationships,
                    financials,
                    competitors
                }, null, 2);
            } catch(e) {
                return JSON.stringify({error: e.message});
            }
        })()
    `);

    try {
        return JSON.parse(data);
    } catch(e) {
        return { error: `parse error: ${e.message}`, raw: data };
    }
}

async function scrapeCompany(companyId, companyName) {
    try {
        // Navigate to profile
        const profileUrl = `https://app.hoovers.dnb.com/company/${companyId}`;
        await navigate(profileUrl);

        // Wait and check
        await new Promise(r => setTimeout(r, 1000));

        const url = await evalJs('window.location.href');
        if (url.includes('/search/company')) {
            // Redirected back to search - try going directly
            console.error(`  [REDIRECT] ${companyName} -> search, trying alternate...`);
            // The profile URL format might be different
            return { source_name: companyName, hoovers_id: companyId, error: 'redirect_to_search' };
        }

        const pageData = await getPageData();

        return {
            source_name: companyName,
            hoovers_id: companyId,
            ...pageData
        };
    } catch(e) {
        return { source_name: companyName, hoovers_id: companyId, error: e.message };
    }
}

async function main() {
    const inputFile = process.argv[2] || 'california_top500_enriched.csv';
    const outputFile = process.argv[3] || 'california_full_profiles.json';
    const limit = parseInt(process.argv[4] || '500');

    console.error(`Connecting to Chrome...`);
    await connect();
    console.error(`Connected. Scraping up to ${limit} companies from ${inputFile}...`);

    // Load companies from CSV
    const companies = [];
    const fileContent = fs.readFileSync(inputFile, 'utf-8');
    const lines = fileContent.split('\n').slice(1); // Skip header
    for (const line of lines) {
        if (!line.trim()) continue;
        const parts = line.split(',');
        if (parts.length >= 9) {
            companies.push({
                source_name: parts[0].replace(/"/g, ''),
                hoovers_id: parts[8].replace(/"/g, '').replace(/\r/, '')
            });
        }
        if (companies.length >= limit) break;
    }

    console.error(`Loaded ${companies.length} companies`);

    const results = [];
    for (let i = 0; i < companies.length; i++) {
        const c = companies[i];
        process.stdout.write(`[${i+1}/${companies.length}] ${c.source_name}... `);

        const data = await scrapeCompany(c.hoovers_id, c.source_name);

        if (data.error && data.error === 'redirect_to_search') {
            // Try alternate URL format
            console.error(`  retrying...`);
            const altData = await scrapeCompany(c.hoovers_id, c.source_name);
            results.push(altData);
        } else {
            results.push(data);
        }

        const hasError = data.error || (data.overview && data.overview.error);
        console.error(hasError ? `ERROR: ${hasError}` : `OK`);

        // Progress checkpoint
        if ((i + 1) % 25 === 0) {
            fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
            console.error(`  [CHECKPOINT ${i+1} saved]`);
        }

        // Rate limit
        await new Promise(r => setTimeout(r, 1500));
    }

    fs.writeFileSync(outputFile, JSON.stringify(results, null, 2));
    console.error(`\nDone. Saved ${results.length} profiles to ${outputFile}`);

    // Summary stats
    const withData = results.filter(r => !r.error);
    const withContacts = withData.filter(r => r.contacts && r.contacts.length > 0);
    const withExecs = withData.filter(r => r.executives && r.executives.length > 0);
    const withCompetitors = withData.filter(r => r.competitors && r.competitors.length > 0);

    console.error(`\nSummary:`);
    console.error(`  Total: ${results.length}`);
    console.error(`  With data: ${withData.length}`);
    console.error(`  With contacts: ${withContacts.length}`);
    console.error(`  With executives: ${withExecs.length}`);
    console.error(`  With competitors: ${withCompetitors.length}`);

    ws.close();
}

main().catch(e => { console.error('FATAL:', e.message); if (ws) ws.close(); process.exit(1); });
