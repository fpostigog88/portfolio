(() => {
  "use strict";

  const actionMeta = {
    audit: {
      button: "Run readiness audit",
      title: "Investment readiness"
    },
    investor: {
      button: "Simulate investment committee",
      title: "Investor committee simulation"
    },
    raise: {
      button: "Build raise plan",
      title: "Seed raise operating plan"
    }
  };

  const syntheticExample = {
    company: "BridgePath Financial",
    product: "A regulated financial product that helps early-career professionals build a transition fund through fixed monthly contributions. Distribution is planned through employers, community organizations, and financial advisers. Revenue comes from origination and ongoing servicing economics.",
    raiseAmount: "4",
    stage: "Seed",
    investorType: "Impact-first family office",
    evidence: "Customer evidence includes 620 survey responses, 58 percent high intent, and 18 completed customer interviews. Two regional employers and one community organization have signed nonbinding letters of intent. Securities counsel produced an initial regulatory pathway memo, but no filing has been submitted. The model assumes 4,800 funded contracts in the first 18 months, a 7 percent referral-to-funded conversion rate, and positive contribution margin after 2,200 active contracts. The company has not yet completed a paid pilot. Impact is currently measured through financial resilience and employment-transition outcomes, but the measurement methodology has not been independently validated. The founder has active conversations with six impact investors but no anchor commitment."
  };

  const sampleResults = {
    audit: {
      summary: "The opportunity has a credible impact narrative and early channel evidence, but it is not yet fully underwritable. The largest gaps are regulatory sequencing, conversion evidence, and proof that the operating model can support the projected volume.",
      overall_score: 61,
      dimensions: [
        { name: "Market evidence", score: 72, rationale: "Survey and interview evidence support interest, but willingness to pay and funded conversion remain unproven.", evidence_needed: "Paid pilot results and segment-level conversion data" },
        { name: "Unit economics", score: 58, rationale: "The model has defined assumptions, but key conversion and servicing-cost inputs are not validated.", evidence_needed: "Bottom-up cost-to-serve analysis and sensitivity cases" },
        { name: "Regulatory readiness", score: 48, rationale: "Counsel has outlined a pathway, but the filing plan, dependencies, budget, and timeline are not investment-grade.", evidence_needed: "Counsel-confirmed regulatory workplan and milestone budget" },
        { name: "Distribution", score: 68, rationale: "Channel interest exists through letters of intent, but activation mechanics and partner incentives are incomplete.", evidence_needed: "Pilot scope, partner economics, and implementation owners" },
        { name: "Impact case", score: 66, rationale: "The intended outcomes are relevant, but attribution and measurement standards need definition.", evidence_needed: "Theory of change, baselines, and reporting methodology" },
        { name: "Operating capacity", score: 54, rationale: "The projected contract volume exceeds the evidence available on process design and staffing capacity.", evidence_needed: "Capacity model, control map, and hiring sequence" }
      ],
      top_risks: [
        "Regulatory timing could consume more capital than the current use-of-funds plan assumes.",
        "The first-year volume target depends on an unvalidated referral-to-funded conversion rate.",
        "Channel letters may not convert without defined economics, compliance ownership, and implementation resources."
      ],
      next_actions: [
        "Convert one channel letter into a scoped pilot with measurable activation and conversion milestones.",
        "Build a regulatory critical path with counsel, costs, dependencies, and investor-visible decision gates.",
        "Rebuild the model around downside, base, and upside cases tied to evidence confidence."
      ]
    },
    investor: {
      recommendation: "Proceed to diligence with conditions",
      confidence: 67,
      thesis: "The company addresses a meaningful financial-transition gap and may fit an impact-first mandate, but the investment should be staged against regulatory and pilot milestones.",
      reasons_to_invest: [
        "Clear beneficiary problem with a measurable financial-resilience outcome.",
        "Potential distribution leverage through employers and community partners.",
        "Impact-first capital could unlock regulatory and pilot milestones before conventional capital is ready."
      ],
      reasons_to_decline: [
        "No paid pilot has demonstrated funded conversion or retention.",
        "The regulatory path remains a memo rather than an executable plan.",
        "The operating model is not yet validated at the proposed contract volume."
      ],
      diligence_questions: [
        "Which assumptions drive cash requirements if regulatory approval is delayed by six months?",
        "What legal and operating responsibilities remain with channel partners versus the company?",
        "How will impact outcomes be measured against a credible baseline?",
        "What evidence supports the first 2,200 active contracts required for contribution margin?",
        "What investor protections and governance rights are appropriate before regulatory clearance?"
      ],
      conditions: [
        "Anchor funding released in tranches tied to regulatory and pilot milestones.",
        "Board-approved downside liquidity plan.",
        "Executed pilot agreement with one channel partner.",
        "Independent review of impact measurement methodology."
      ]
    },
    raise: {
      objective: "Secure an impact-first anchor, validate the highest-risk assumptions during diligence, and close the remaining syndicate around a milestone-based use of funds.",
      phases: [
        {
          name: "Investment readiness",
          outcome: "One underwritable data room and management narrative",
          actions: ["Reconcile the model, regulatory plan, impact case, and use of funds", "Build downside scenarios and a diligence issue log", "Define the exact milestones the Seed capital purchases"]
        },
        {
          name: "Anchor formation",
          outcome: "A lead investor aligned to early regulatory and market risk",
          actions: ["Prioritize investors by mandate, check size, and catalytic fit", "Sequence warm introductions through the founder and advisers", "Use investor feedback to resolve objections before broad outreach"]
        },
        {
          name: "Syndicate close",
          outcome: "A coordinated round with clear allocation and decision timing",
          actions: ["Run meetings in concentrated waves", "Centralize diligence responses and version control", "Move aligned investors toward rolling or milestone-linked closes"]
        }
      ],
      syndicate_strategy: [
        "Target a 30 to 45 percent anchor from an impact-first family office or catalytic investor.",
        "Use mission-aligned funds for the core financial return and impact case.",
        "Reserve strategic allocation for investors that strengthen distribution, credibility, or later capital formation."
      ],
      weekly_cadence: [
        "Monday pipeline and diligence review with the Founder and CEO.",
        "Midweek investor meetings and same-day objection capture.",
        "Friday decision review covering probability, blockers, owners, and next commitments."
      ],
      milestones: [
        "Complete investment-readiness work before broad market outreach.",
        "Secure anchor-level interest before opening the full syndicate.",
        "Close the round against defined regulatory, pilot, and operating milestones."
      ]
    }
  };

  const tabs = Array.from(document.querySelectorAll(".mode-tab"));
  const form = document.getElementById("agent-form");
  const companyInput = document.getElementById("company-name");
  const productInput = document.getElementById("product-summary");
  const raiseInput = document.getElementById("raise-amount");
  const stageInput = document.getElementById("stage");
  const investorInput = document.getElementById("investor-type");
  const evidenceInput = document.getElementById("evidence");
  const loadExampleButton = document.getElementById("load-example");
  const previewButton = document.getElementById("preview-sample");
  const runButton = document.getElementById("run-agent");
  const runButtonLabel = runButton.querySelector(".button-label");
  const resultsPanel = document.querySelector(".results-panel");
  const resultsTitle = document.getElementById("results-title");
  const resultStatus = document.getElementById("result-status");
  const emptyState = document.getElementById("results-empty");
  const resultsContent = document.getElementById("results-content");

  let activeAction = "audit";

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => setAction(tab.dataset.action));
  });

  loadExampleButton.addEventListener("click", () => {
    companyInput.value = syntheticExample.company;
    productInput.value = syntheticExample.product;
    raiseInput.value = syntheticExample.raiseAmount;
    stageInput.value = syntheticExample.stage;
    investorInput.value = syntheticExample.investorType;
    evidenceInput.value = syntheticExample.evidence;
  });

  previewButton.addEventListener("click", () => {
    renderResult(activeAction, sampleResults[activeAction], true);
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = collectPayload();
    const validationError = validatePayload(payload);

    if (validationError) {
      renderError(validationError);
      return;
    }

    await runAnalysis(payload);
  });

  function setAction(action) {
    if (!actionMeta[action]) return;

    activeAction = action;
    tabs.forEach((tab) => {
      const isActive = tab.dataset.action === action;
      tab.classList.toggle("active", isActive);
      tab.setAttribute("aria-selected", String(isActive));
    });

    runButtonLabel.textContent = actionMeta[action].button;
    resultsTitle.textContent = actionMeta[action].title;
  }

  function collectPayload() {
    return {
      action: activeAction,
      company: companyInput.value.trim(),
      product: productInput.value.trim(),
      raiseAmount: Number(raiseInput.value),
      stage: stageInput.value,
      investorType: investorInput.value,
      evidence: evidenceInput.value.trim()
    };
  }

  function validatePayload(payload) {
    if (!payload.company) return "Add the company or project name.";
    if (payload.product.length < 40) return "Add a clearer product and business-model description.";
    if (!Number.isFinite(payload.raiseAmount) || payload.raiseAmount <= 0) return "Add a valid target raise.";
    if (payload.evidence.length < 80) return "Add enough evidence for the agent to evaluate the opportunity.";
    return "";
  }

  async function runAnalysis(payload) {
    setLoading(true);

    try {
      const response = await fetch("/api/ngbc/capital-readiness", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || "The agent could not complete the analysis.");
      }

      renderResult(data.action || activeAction, data.result, false);
    } catch (error) {
      renderError(error instanceof Error ? error.message : "The agent could not complete the analysis.");
    } finally {
      setLoading(false);
    }
  }

  function setLoading(isLoading) {
    resultsPanel.setAttribute("aria-busy", String(isLoading));
    runButton.disabled = isLoading;
    resultStatus.className = `status-pill${isLoading ? " loading" : ""}`;
    resultStatus.textContent = isLoading ? "Analyzing" : "Ready";
    if (isLoading) {
      runButtonLabel.textContent = "Analyzing evidence";
    } else {
      runButtonLabel.textContent = actionMeta[activeAction].button;
    }
  }

  function renderResult(action, result, isSample) {
    emptyState.hidden = true;
    resultsContent.hidden = false;
    resultsContent.replaceChildren();
    resultsTitle.textContent = actionMeta[action]?.title || "Agent output";
    resultStatus.className = "status-pill";
    resultStatus.textContent = isSample ? "Sample" : "Complete";

    if (action === "audit") renderAudit(result);
    if (action === "investor") renderInvestor(result);
    if (action === "raise") renderRaise(result);
  }

  function renderAudit(result) {
    resultsContent.appendChild(
      summaryCard("Readiness assessment", result.summary, result.overall_score)
    );

    const dimensions = section("Readiness dimensions");
    const dimensionGrid = element("div", "dimension-grid");
    toArray(result.dimensions).forEach((dimension) => {
      const card = element("article", "dimension-card");
      const head = element("div", "dimension-head");
      head.appendChild(textElement("h4", dimension.name || "Dimension"));
      head.appendChild(textElement("span", `${numberOrZero(dimension.score)}/100`, "dimension-score"));
      card.appendChild(head);
      card.appendChild(textElement("p", dimension.rationale || "No rationale returned."));
      card.appendChild(textElement("div", `Evidence needed  ${dimension.evidence_needed || "Not specified"}`, "evidence-needed"));
      dimensionGrid.appendChild(card);
    });
    dimensions.appendChild(dimensionGrid);
    resultsContent.appendChild(dimensions);

    resultsContent.appendChild(listSection("Top risks", result.top_risks));
    resultsContent.appendChild(listSection("Next actions", result.next_actions));
  }

  function renderInvestor(result) {
    resultsContent.appendChild(
      summaryCard(result.recommendation || "Investment committee view", result.thesis, result.confidence)
    );

    const grid = element("div", "result-grid");
    grid.appendChild(listCard("Reasons to invest", result.reasons_to_invest));
    grid.appendChild(listCard("Reasons to decline", result.reasons_to_decline));
    resultsContent.appendChild(grid);
    resultsContent.appendChild(listSection("Diligence questions", result.diligence_questions));
    resultsContent.appendChild(listSection("Conditions before commitment", result.conditions));
  }

  function renderRaise(result) {
    resultsContent.appendChild(summaryCard("Closing objective", result.objective));

    const phasesSection = section("Raise phases");
    const phaseGrid = element("div", "phase-grid");
    toArray(result.phases).forEach((phase, index) => {
      const card = element("article", "phase-card");
      const head = element("div", "phase-head");
      head.appendChild(textElement("h4", phase.name || `Phase ${index + 1}`));
      head.appendChild(textElement("span", String(index + 1).padStart(2, "0"), "phase-number"));
      card.appendChild(head);
      card.appendChild(textElement("p", phase.outcome || ""));
      card.appendChild(buildList(phase.actions));
      phaseGrid.appendChild(card);
    });
    phasesSection.appendChild(phaseGrid);
    resultsContent.appendChild(phasesSection);

    resultsContent.appendChild(listSection("Syndicate strategy", result.syndicate_strategy));
    resultsContent.appendChild(listSection("Weekly operating cadence", result.weekly_cadence));
    resultsContent.appendChild(listSection("Closing milestones", result.milestones));
  }

  function renderError(message) {
    emptyState.hidden = true;
    resultsContent.hidden = false;
    resultsContent.replaceChildren();
    resultStatus.className = "status-pill error";
    resultStatus.textContent = "Action needed";

    const box = element("div", "error-box");
    box.appendChild(textElement("h3", "Could not run the analysis"));
    box.appendChild(textElement("p", message));
    resultsContent.appendChild(box);
  }

  function summaryCard(title, body, score) {
    const card = element("section", "result-summary");
    card.appendChild(textElement("span", "Executive view", "result-kicker"));
    card.appendChild(textElement("h3", title || "Assessment"));
    card.appendChild(textElement("p", body || "No summary returned."));

    if (Number.isFinite(Number(score))) {
      const normalizedScore = Math.max(0, Math.min(100, Number(score)));
      const row = element("div", "score-row");
      row.appendChild(textElement("span", String(Math.round(normalizedScore)), "score-number"));
      const track = element("div", "score-track");
      const fill = element("span");
      fill.style.width = `${normalizedScore}%`;
      track.appendChild(fill);
      row.appendChild(track);
      card.appendChild(row);
    }

    return card;
  }

  function listCard(title, items) {
    const card = element("article", "result-card");
    card.appendChild(textElement("h4", title));
    card.appendChild(buildList(items));
    return card;
  }

  function listSection(title, items) {
    const wrapper = section(title);
    wrapper.appendChild(buildList(items));
    return wrapper;
  }

  function section(title) {
    const wrapper = element("section", "result-section");
    wrapper.appendChild(textElement("h3", title, "result-section-title"));
    return wrapper;
  }

  function buildList(items) {
    const list = element("ul", "result-list");
    const normalizedItems = toArray(items);
    if (!normalizedItems.length) {
      normalizedItems.push("No items returned.");
    }
    normalizedItems.forEach((item) => list.appendChild(textElement("li", String(item))));
    return list;
  }

  function element(tagName, className = "") {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    return node;
  }

  function textElement(tagName, text, className = "") {
    const node = element(tagName, className);
    node.textContent = text ?? "";
    return node;
  }

  function toArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function numberOrZero(value) {
    const number = Number(value);
    return Number.isFinite(number) ? Math.max(0, Math.min(100, Math.round(number))) : 0;
  }
})();
