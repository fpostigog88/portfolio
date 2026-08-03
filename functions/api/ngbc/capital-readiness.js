/**
 * NGBC Capital Readiness API
 * POST /api/capital-readiness
 * Protected by session middleware — unauthenticated requests never reach this handler.
 *
 * Workers AI binding: AI (configured in Cloudflare Pages settings)
 * Falls back to structured keyword-analysis when AI is unavailable.
 */

const MAX_BODY_BYTES = 28_000;

export async function onRequestPost(context) {
  const requestId = crypto.randomUUID();

  try {
    // Size limits
    const contentLength = Number(context.request.headers.get("Content-Length") || 0);
    if (contentLength > MAX_BODY_BYTES) {
      return jsonResponse(
        { error: "The submitted evidence is too large.", code: "PAYLOAD_TOO_LARGE", requestId },
        413
      );
    }

    const rawBody = await context.request.text();
    if (new TextEncoder().encode(rawBody).byteLength > MAX_BODY_BYTES) {
      return jsonResponse(
        { error: "The submitted evidence is too large.", code: "PAYLOAD_TOO_LARGE", requestId },
        413
      );
    }

    // Parse and validate
    let payload;
    try {
      payload = JSON.parse(rawBody);
    } catch {
      return jsonResponse(
        { error: "The request body must be valid JSON.", code: "INVALID_JSON", requestId },
        400
      );
    }

    const validationError = validatePayload(payload);
    if (validationError) {
      return jsonResponse({ error: validationError, code: "INVALID_INPUT", requestId }, 400);
    }

    let result;
    let mode = "structured-fallback";

    if (context.env.AI) {
      try {
        const prompt = buildPrompt(payload);
        const schema = schemas[payload.action];

        const answer = await context.env.AI.run(MODEL, {
          messages: [
            { role: "system", content: systemPrompts[payload.action] },
            { role: "user", content: prompt }
          ],
          response_format: {
            type: "json_schema",
            json_schema: schema
          }
        });

        if (!answer || typeof answer !== "object" || !("response" in answer)) {
          throw new Error("Workers AI returned an unexpected response shape.");
        }

        result = answer.response;
        mode = "workers-ai";
      } catch (aiErr) {
        console.error(`Workers AI error: ${aiErr instanceof Error ? aiErr.message : aiErr}`);
        // Fall through to fallback
      }
    }

    if (!result) {
      result = buildFallbackResult(payload);
      mode = "structured-fallback";
    }

    console.log(JSON.stringify({
      event: "capital_agent_completed",
      requestId,
      action: payload.action,
      stage: payload.stage,
      investorType: payload.investorType,
      mode
    }));

    return jsonResponse({ action: payload.action, result, requestId, mode }, 200);

  } catch (error) {
    console.error(JSON.stringify({
      event: "capital_agent_failed",
      requestId,
      message: error instanceof Error ? error.message : "Unknown error"
    }));

    const message = error instanceof Error && error.message.includes("JSON Mode")
      ? "The model could not produce the required structured output. Try again with clearer evidence."
      : "The agent could not complete the analysis.";

    return jsonResponse({ error: message, code: "AGENT_ERROR", requestId }, 500);
  }
}

export function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      Allow: "POST, OPTIONS",
      "Cache-Control": "no-store"
    }
  });
}

function validatePayload(payload) {
  if (!payload || typeof payload !== "object") return "A request payload is required.";
  if (!ALLOWED_ACTIONS.has(payload.action)) return "Select a valid analysis type.";
  if (!isStringInRange(payload.company, 1, 120)) return "Add the company or project name.";
  if (!isStringInRange(payload.product, 40, 1800)) return "Add a clearer product and business-model description.";
  if (!Number.isFinite(payload.raiseAmount) || payload.raiseAmount <= 0 || payload.raiseAmount > 1000) return "Add a valid target raise.";
  if (!isStringInRange(payload.stage, 1, 50)) return "Select a valid fundraising stage.";
  if (!isStringInRange(payload.investorType, 1, 100)) return "Select an investor lens.";
  if (!isStringInRange(payload.evidence, 80, 12000)) return "Add enough evidence for the analysis.";
  return "";
}

function isStringInRange(value, min, max) {
  return typeof value === "string" && value.trim().length >= min && value.trim().length <= max;
}

function buildPrompt(payload) {
  return [
    `Company or project: ${payload.company}`,
    `Fundraising stage: ${payload.stage}`,
    `Target raise: $${payload.raiseAmount} million`,
    `Investor lens: ${payload.investorType}`,
    "",
    "Product and business model",
    payload.product,
    "",
    "Current evidence and open questions",
    payload.evidence,
    "",
    "Use only the information above. Treat every missing fact as missing evidence rather than filling the gap."
  ].join("\n");
}

function jsonResponse(body, status) {
  return Response.json(body, {
    status,
    headers: {
      "Cache-Control": "no-store",
      "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'",
      "X-Content-Type-Options": "nosniff"
    }
  });
}

function buildFallbackResult(payload) {
  const text = `${payload.product}\n${payload.evidence}`.toLowerCase();
  const signals = {
    market: countSignals(text, ["survey", "interview", "pilot", "customer", "intent", "waitlist"]),
    economics: countSignals(text, ["unit economics", "contribution margin", "cac", "ltv", "revenue", "conversion", "break-even", "breakeven"]),
    regulatory: countSignals(text, ["regulation", "regulatory", "counsel", "filing", "sec", "compliance", "audit"]),
    distribution: countSignals(text, ["partner", "partnership", "distribution", "advisor", "bank", "employer", "channel", "letter of intent", "loi"]),
    impact: countSignals(text, ["impact", "outcome", "measurement", "theory of change", "beneficiary", "underserved"]),
    operations: countSignals(text, ["operations", "capacity", "processing", "team", "workflow", "quality assurance", "controls"])
  };

  const scoreFor = (value) => Math.min(85, 25 + value * 12);
  const overall = Math.round(
    Object.values(signals).reduce((sum, value) => sum + scoreFor(value), 0) / 6
  );

  if (payload.action === "audit") {
    const dimensions = [
      ["Market evidence", signals.market, "customer demand and adoption evidence", "a paid pilot, cohort conversion data, and customer references"],
      ["Unit economics", signals.economics, "revenue logic and contribution economics", "a driver-based model with downside cases, CAC, conversion, servicing cost, and cash needs"],
      ["Regulatory readiness", signals.regulatory, "legal and compliance preparation", "written counsel conclusions, filing sequence, audited-financial requirements, and accountable owners"],
      ["Distribution", signals.distribution, "channel access and partner evidence", "signed agreements, referral economics, implementation plans, and partner-level volume assumptions"],
      ["Impact case", signals.impact, "mission and outcome evidence", "a theory of change, baseline, measurable outcomes, attribution logic, and reporting cadence"],
      ["Operating capacity", signals.operations, "the ability to execute at the proposed scale", "a capacity model, controls, hiring sequence, service levels, and failure-mode plans"]
    ].map(([name, value, subject, needed]) => ({
      name,
      score: scoreFor(value),
      rationale: value >= 3
        ? `The submission contains several references to ${subject}, but institutional diligence will still test the quality and traceability of that evidence.`
        : `The submission provides limited support for ${subject}. This will likely remain an investment committee concern.`,
      evidence_needed: `Provide ${needed}.`
    }));

    return {
      summary:
        overall >= 65
          ? "The opportunity has a credible starting case, but the round should be sequenced around closing the remaining evidence gaps before broad outreach."
          : "The opportunity is not yet fully underwritable. The next step is to convert major assumptions into documented evidence before running a broad institutional process.",
      overall_score: overall,
      dimensions,
      top_risks: [
        "Investor diligence may expose assumptions that are not yet supported by executed evidence.",
        "The regulatory, distribution, and operating milestones may require more capital or time than the current plan assumes.",
        "Mission alignment alone will not resolve questions about repeatable economics and execution capacity."
      ],
      next_actions: [
        "Create one diligence tracker linking every investor claim to a source document, owner, and update date.",
        "Build a downside case showing the cash and milestone impact of slower conversion, higher operating cost, and regulatory delay.",
        "Define the minimum evidence required before anchor outreach and separate it from evidence that can be completed during diligence.",
        "Translate impact goals into measurable outcomes that can be reported consistently to investors."
      ]
    };
  }

  if (payload.action === "investor") {
    return {
      recommendation: overall >= 70 ? "Proceed to focused diligence" : "Defer commitment pending evidence milestones",
      confidence: Math.min(90, Math.max(45, overall)),
      thesis: `For a ${payload.investorType}, the strongest case is the combination of mission alignment, a potentially scalable distribution model, and the ability to use a $${payload.raiseAmount}M ${payload.stage} round to retire specific regulatory, commercial, and operating risks.`,
      reasons_to_invest: [
        "The product addresses a defined transition or resilience need with a model intended to scale through institutional channels.",
        "The raise can be tied to concrete de-risking milestones rather than an open-ended operating plan.",
        "An impact-first investor may be able to provide catalytic capital and credibility that improves the remaining syndicate."
      ],
      reasons_to_decline: [
        "Key demand, conversion, regulatory, or channel assumptions may not yet be proven through executed evidence.",
        "The capital required to reach sustainable economics may exceed the current round.",
        "Impact measurement may not yet distinguish intended outcomes from evidence of attributable results."
      ],
      diligence_questions: [
        "Which assumptions drive the majority of enterprise value and what evidence supports each one?",
        "What exact regulatory milestones must be completed before commercial launch and who owns them?",
        "What partner commitments are signed, what are the economics, and what implementation work remains?",
        "What happens to runway and milestones if conversion is half the base case?",
        "How will impact outcomes be measured, verified, and reported?",
        "Which risks must an anchor investor accept and which should be retired before commitment?"
      ],
      conditions: [
        "Complete a source-linked diligence room and reconcile all financial, legal, commercial, and impact claims.",
        "Secure written validation of the regulatory sequence and related cost and timing assumptions.",
        "Demonstrate channel and customer traction through signed commitments or a controlled pilot.",
        "Agree on governance, reporting, and milestone-based use of proceeds."
      ]
    };
  }

  return {
    objective: `Close a $${payload.raiseAmount}M ${payload.stage} round by making the company underwritable, securing an aligned anchor, and coordinating the remaining investors through one controlled diligence process.`,
    phases: [
      {
        name: "Investment readiness",
        outcome: "A consistent, source-linked investment case that can survive institutional diligence.",
        actions: [
          "Reconcile the financial model, regulatory plan, distribution assumptions, impact framework, and use of funds.",
          "Create a claim-to-evidence matrix and resolve contradictions before investor circulation.",
          "Define the milestones this round buys and the downside case if timing or conversion misses plan."
        ]
      },
      {
        name: "Anchor process",
        outcome: "A credible lead investor able to validate the opportunity and establish momentum.",
        actions: [
          `Prioritize ${payload.investorType} prospects whose mandate matches the risk and impact profile.`,
          "Sequence the strongest warm relationships first and ask for a defined diligence decision rather than general feedback.",
          "Use objections to improve the company and data room without allowing the process to fragment."
        ]
      },
      {
        name: "Syndication and close",
        outcome: "Remaining allocations move through coordinated diligence toward signed commitments.",
        actions: [
          "Run concentrated meeting waves with one message, one data room, and one owner for every follow-up.",
          "Track check size, mandate fit, objections, requested materials, decision process, probability, and next action.",
          "Use rolling closes only when they strengthen momentum and do not create conflicting terms."
        ]
      }
    ],
    syndicate_strategy: [
      "Use an impact-first anchor to absorb early regulatory and market-development risk.",
      "Add mission-aligned funds that can underwrite both financial return and measurable impact.",
      "Reserve strategic allocation for investors that strengthen distribution, operating credibility, or later capital formation."
    ],
    weekly_cadence: [
      "Monday review of pipeline movement, diligence requests, model changes, and decisions needed from the Founder and CEO.",
      "Same-day meeting notes, objection capture, owner assignment, and follow-up delivery.",
      "Friday closing review covering probability, blockers, next commitments, and the following week's meeting sequence."
    ],
    milestones: [
      "Complete investment-readiness work before broad institutional outreach.",
      "Secure anchor-level interest before opening the full syndicate.",
      "Close the round against defined regulatory, pilot, distribution, and operating milestones."
    ]
  };
}

function countSignals(text, terms) {
  return terms.reduce((count, term) => count + (text.includes(term) ? 1 : 0), 0);
}

const ALLOWED_ACTIONS = new Set(["audit", "investor", "raise"]);

const MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";

const systemPrompts = {
  audit: [
    "You are the diligence lead for an institutional impact and impact-first Seed investment committee.",
    "Evaluate whether the company is underwritable today across market evidence, unit economics, regulatory readiness, distribution, impact case, and operating capacity.",
    "Use only the submitted evidence. Do not invent facts, legal conclusions, market benchmarks, or investor commitments.",
    "Score each dimension based on evidence quality, not presentation quality.",
    "Be direct, commercially rigorous, and specific about what would change the investment decision."
  ].join(" "),
  investor: [
    "You are an investment committee evaluating a Seed opportunity through the investor mandate provided by the user.",
    "Return a balanced recommendation, the strongest investment thesis, the strongest reasons to decline, the most important diligence questions, and conditions required before commitment.",
    "Use only the submitted evidence. Do not invent facts, legal conclusions, market benchmarks, or investor commitments.",
    "Distinguish mission alignment from evidence that the company can produce financial and impact outcomes."
  ].join(" "),
  raise: [
    "You are a President-level fundraising operating partner helping a Founder and CEO close an institutional Seed round.",
    "Build a practical plan that makes the company underwritable, secures the right anchor, and runs the remaining syndicate through coordinated diligence and closing.",
    "Use only the submitted evidence. Do not invent investor names, commitments, legal conclusions, or market benchmarks.",
    "The plan must convert current gaps into sequencing, milestones, owners, and a weekly operating cadence."
  ].join(" ")
};

const schemas = {
  audit: {
    type: "object",
    additionalProperties: false,
    properties: {
      summary: { type: "string" },
      overall_score: { type: "integer", minimum: 0, maximum: 100 },
      dimensions: {
        type: "array",
        minItems: 6,
        maxItems: 6,
        items: {
          type: "object",
          additionalProperties: false,
          properties: {
            name: { type: "string" },
            score: { type: "integer", minimum: 0, maximum: 100 },
            rationale: { type: "string" },
            evidence_needed: { type: "string" }
          },
          required: ["name", "score", "rationale", "evidence_needed"]
        }
      },
      top_risks: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } },
      next_actions: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } }
    },
    required: ["summary", "overall_score", "dimensions", "top_risks", "next_actions"]
  },
  investor: {
    type: "object",
    additionalProperties: false,
    properties: {
      recommendation: { type: "string" },
      confidence: { type: "integer", minimum: 0, maximum: 100 },
      thesis: { type: "string" },
      reasons_to_invest: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } },
      reasons_to_decline: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } },
      diligence_questions: { type: "array", minItems: 5, maxItems: 8, items: { type: "string" } },
      conditions: { type: "array", minItems: 3, maxItems: 6, items: { type: "string" } }
    },
    required: ["recommendation", "confidence", "thesis", "reasons_to_invest", "reasons_to_decline", "diligence_questions", "conditions"]
  },
  raise: {
    type: "object",
    additionalProperties: false,
    properties: {
      objective: { type: "string" },
      phases: {
        type: "array",
        minItems: 3,
        maxItems: 4,
        items: {
          type: "object",
          additionalProperties: false,
          properties: {
            name: { type: "string" },
            outcome: { type: "string" },
            actions: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } }
          },
          required: ["name", "outcome", "actions"]
        }
      },
      syndicate_strategy: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } },
      weekly_cadence: { type: "array", minItems: 3, maxItems: 5, items: { type: "string" } },
      milestones: { type: "array", minItems: 3, maxItems: 6, items: { type: "string" } }
    },
    required: ["objective", "phases", "syndicate_strategy", "weekly_cadence", "milestones"]
  }
};
