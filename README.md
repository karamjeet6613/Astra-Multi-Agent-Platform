<div align="center">

# Astra AI — Enterprise Multi-Agent Platform
### 5 Production AI Modules · LangGraph · RAGAS · HITL · Live on Streamlit

[![Live Demo](https://img.shields.io/badge/▶_Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://astra-ai-enterprise-multi-agent-revenue-intelligence-platform.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-karamjeetsingh--ai--pm-181717?style=for-the-badge&logo=github)](https://github.com/karamjeetsingh-ai-pm/Astra-Multi-Agent-Platform)
[![Website](https://img.shields.io/badge/Website-karamjeetsingh.com-000?style=for-the-badge)](https://www.karamjeetsingh.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Stack:** Streamlit · LangGraph · CrewAI · Groq LLaMA 3 · Gemini · Supabase · RAGAS · Tavily · Apollo.io · Python

</div>

---

## 🗺️ Platform Overview

Astra is a multi-module AI platform built to demonstrate **what production enterprise AI actually looks like** — not a chatbot demo, but a full platform with agent orchestration, RAG pipelines, evals, HITL design, and observability.

Each module solves a real enterprise problem. Together they show the full AI PM stack: from user-facing interfaces to the governance layer underneath.

**Navigate to a module:**

| Module | Jump To |
|--------|---------|
| 1. Enterprise Revenue Intelligence | [→ Jump](#1-enterprise-revenue-intelligence) |
| 2. Enterprise SDR Agent | [→ Jump](#2-enterprise-sdr-agent) |
| 3. Multi-Agent Command Centre | [→ Jump](#3-multi-agent-command-centre) |
| 4. AskHR Policy Assistant | [→ Jump](#4-askhr-policy-assistant) |
| 5. Evals & Observability | [→ Jump](#5-evals--observability) |

---

## 1. Enterprise Revenue Intelligence

**`Revenue Leaders fly blind — dashboards show what happened, not what to do next.`**

### The Problem
AEs track deals in CRMs. CFOs track P&L in spreadsheets. Neither view is connected to AI that tells you what to do. Revenue intelligence platforms exist but they're expensive, rigid, and don't explain their recommendations.

### What It Does
A unified AI revenue platform with two personas in one interface:
- **AE View** — live pipeline, at-risk deal alerts, rep leaderboard, AI-recommended next best action
- **CFO View** — P&L summary, margin tracking, NRR trends, OpEx breakdown, CFO Copilot natural language chat

### Architecture
```
User Query / Dashboard Load
        │
   Persona Router (AE / CFO toggle)
        │
   ┌────┴────────────────────┐
   │                         │
AE Pipeline Engine     CFO Analytics Engine
(Supabase · LangGraph)  (Supabase · Gemini)
   │                         │
Deal Risk Scorer        CFO Copilot RAG
(LLM + rules engine)   (LangChain · Groq)
   │                         │
   └──────────┬──────────────┘
              │
     Unified Dashboard (Streamlit)
```

### Key Capabilities
- AE pipeline with deal health scoring (Green / At-Risk / Critical)
- Rep performance leaderboard with AI coaching suggestions
- AI next best action per deal — call, email, escalate
- CFO P&L with margin %, NRR, churn rate, OpEx breakdown
- CFO Copilot: natural language queries over financial data
- HITL — AI suggests, revenue leader approves

### PM Design Decisions
- **Two personas, one dataset** — same Supabase tables, different read layers. Avoids data duplication, ensures consistency
- **Risk scoring is rules + LLM, not LLM alone** — rule-based first pass for latency, LLM for explanation generation. Makes the system fast and explainable
- **"Next best action" always shows reasoning** — not just "call the prospect" but why, based on deal stage, last touch, and signal data

### Tech Stack
`Streamlit` `LangGraph` `Groq LLaMA 3` `Gemini` `Supabase` `LangChain` `Python`

[![▶ Launch Module](https://img.shields.io/badge/▶_Launch_Module-Live_Demo-FF4B4B?style=flat-square)](https://astra-ai-enterprise-multi-agent-revenue-intelligence-platform.streamlit.app/)

---

## 2. Enterprise SDR Agent

**`SDRs spend 70% of their time on research and writing, not selling.`**

### The Problem
Sales Development Reps manually research prospects, write personalised emails, track responses, and manage follow-up sequences. At scale this is hours of repetitive work per rep per day — and quality is inconsistent.

### What It Does
A fully autonomous SDR agent that:
1. Sources leads from Apollo.io based on ICP criteria
2. Scores each lead for fit (industry, company size, role, signals)
3. Researches the company and prospect using Tavily web search
4. Drafts a personalised first email + 2-step follow-up sequence
5. Presents to the human SDR for review and one-click approval
6. Tracks the pipeline in a live view

### Architecture
```
ICP Input (industry · size · title · signals)
        │
   Apollo.io Lead Sourcing Agent
        │
   ICP Fit Scorer (LLM + rules)
        │
   Company Research Agent (Tavily)
        │
   Personalisation Agent (Groq LLaMA 3)
        │     ↑
        │  [Company context + signals]
        │
   Email Draft (Subject + Body + 2 follow-ups)
        │
   ╔════▼══════════════╗
   ║  HITL REVIEW      ║  ← SDR reviews, edits, approves
   ╚════┬══════════════╝
        │
   Pipeline Tracker (Supabase)
```

### Key Capabilities
- Apollo.io integration for lead sourcing with ICP filters
- Multi-signal ICP fit scoring (0–100) with explanation
- Tavily-powered real-time company research
- Personalised email generation — not templates, actual context-specific writing
- 2-step follow-up sequence auto-generated
- Human-in-the-loop approval before any outreach
- Live pipeline board with lead status tracking

### PM Design Decisions
- **HITL is non-negotiable** — no autonomous send. The value is in the research and drafting, not in removing human judgment. Any enterprise buyer would reject a system that sends emails without review
- **ICP scoring shows its work** — score + 3 bullet reasons. SDRs trust it because they can audit it
- **Research before personalisation** — the agent queries Tavily *before* writing, not after. Forces the LLM to ground the email in real signals, not generic flattery

### Tech Stack
`Apollo.io` `Tavily Search` `LangGraph` `Groq LLaMA 3` `Streamlit` `Supabase` `Python`

[![▶ Launch Module](https://img.shields.io/badge/▶_Launch_Module-Live_Demo-FF4B4B?style=flat-square)](https://astra-ai-enterprise-multi-agent-revenue-intelligence-platform.streamlit.app/)

---

## 3. Multi-Agent Command Centre

**`Complex enterprise questions span departments — no single tool can answer them.`**

### The Problem
An executive asking "What's our Q3 revenue risk, and do we have the headcount to respond?" needs answers from Sales, Finance, and HR simultaneously. No single AI tool or agent can handle cross-functional queries with the depth each domain requires.

### What It Does
A master orchestrator that:
1. Receives a complex enterprise query
2. Reasons about which domains are involved
3. Decomposes into sub-tasks and routes to specialist agents
4. Runs agents in parallel or sequence (LangGraph)
5. Synthesizes outputs into one executive-ready response
6. Shows full agent reasoning trail — every step is auditable

### Architecture
```
Complex Query Input
        │
   Master Orchestrator (LangGraph Supervisor)
        │
   Task Decomposition + Routing Decision
        │
   ┌────┬──────┬────────┬──────────┐
   │    │      │        │          │
Sales  HR  Finance  Research  (extensible)
Agent  Agent Agent   Agent
   │    │      │        │
   └────┴──────┴────────┘
              │
   Response Synthesis Agent
              │
   Executive Summary + Source Trail
              │
   ╔══════════▼══════════╗
   ║  HITL Review Gate   ║  ← Optional human review
   ╚═════════════════════╝
```

### Key Capabilities
- Natural language task input — no structured forms
- Live agent reasoning display — see each agent's thought process as it runs
- Parallel agent execution where subtasks are independent
- Sequential routing when outputs feed each other
- Domain agents: Sales (pipeline), HR (policy + headcount), Finance (P&L + forecast), Research (web search)
- Full audit trail — every agent decision logged with timestamp
- Synthesis agent produces one coherent, sourced response

### PM Design Decisions
- **Show the reasoning, not just the answer** — enterprises won't trust AI that gives answers without showing its work. Every agent's intermediate output is visible in the UI
- **Supervisor architecture over peer agents** — LangGraph Supervisor pattern gives a single point of orchestration. Prevents agents from contradicting each other or creating infinite loops
- **Extensible agent slots** — designed for new domain agents to be added without touching orchestration logic. Product decision to future-proof the architecture

### Tech Stack
`LangGraph` `CrewAI` `Groq` `Gemini` `Supabase` `Tavily` `Streamlit` `Python`

[![▶ Launch Module](https://img.shields.io/badge/▶_Launch_Module-Live_Demo-FF4B4B?style=flat-square)](https://astra-ai-enterprise-multi-agent-revenue-intelligence-platform.streamlit.app/)

---

## 4. AskHR Policy Assistant

**`Employees waste hours searching policy docs. HR wastes time answering the same questions repeatedly.`**

### The Problem
Every company has HR policy documents — leave policy, compensation, benefits, performance, code of conduct. Employees either can't find the right document, or can't parse the legal language when they do. HR spends 20–30% of time answering questions that are already answered in writing.

### What It Does
A RAG-powered HR assistant that answers any policy question by actually reading the company's HR documents — not generic knowledge, not hallucinated policies. Every answer is cited to the source paragraph.

### Architecture
```
Employee Question (natural language)
        │
   Query Understanding (intent + entity extraction)
        │
   Semantic Search (Supabase vector store)
        │     ← HR PDFs embedded at ingestion
        │
   Top-K Chunk Retrieval (cosine similarity)
        │
   Prompt Assembly (question + context + instructions)
        │
   LLM Response Generation (Groq LLaMA 3)
        │
   Citation Attachment (source doc + paragraph)
        │
   Hallucination Check (does answer match retrieved chunks?)
        │
   Answer + Sources → Employee
```

### Key Capabilities
- Semantic search over HR PDF documents
- Multi-document retrieval — searches across all policy docs simultaneously
- Source citation — every answer shows which document and section it came from
- Covers: leave & PTO, compensation & bonuses, benefits & health, performance reviews, notice periods, code of conduct, expense policies
- Works 24/7 — no HR ticket needed for standard queries
- Sample questions pre-loaded for immediate demo

### PM Design Decisions
- **Citation is mandatory, not optional** — employees need to be able to verify answers against the actual policy. An answer without a source is an unverifiable claim
- **RAG over fine-tuning** — HR policies change quarterly. RAG allows document updates without retraining. Fine-tuning would bake in stale policies
- **Hallucination check before delivery** — the system verifies the generated answer is grounded in the retrieved chunks before returning it. Catches the cases where the LLM "helpfully" adds information not in the documents

### Tech Stack
`Supabase` `LangChain` `Groq LLaMA 3` `Streamlit` `Python` `PDF parsing`

[![▶ Launch Module](https://img.shields.io/badge/▶_Launch_Module-Live_Demo-FF4B4B?style=flat-square)](https://astra-ai-enterprise-multi-agent-revenue-intelligence-platform.streamlit.app/)

---

## 5. Evals & Observability

**`Enterprises can't trust AI systems they can't measure.`**

### The Problem
Most AI demos look good until they don't. Without an evaluation framework, there's no way to know if a RAG system is hallucinating 3% of the time or 30%. Without observability, you can't catch model drift before it becomes a business incident.

### What It Does
A full AI quality assurance platform with:
- **RAGAS evaluation** — automated scoring across faithfulness, answer relevancy, context recall, and context precision
- **Hallucination demo** — intentionally triggers hallucinations to show how the detection layer catches them
- **Red-teaming interface** — test adversarial inputs and edge cases
- **Drift monitoring** — tracks metric trends over time, alerts on statistical deviation

### Architecture
```
AI System Output
        │
   ┌────┴──────────────────────────┐
   │                               │
RAGAS Evaluation Pipeline    Observability Layer
        │                          │
   ┌────┴────────────────┐    Langfuse / Evidently AI
   │         │           │         │
Faithfulness Answer   Context   Drift Detection
Score     Relevancy   Precision  (2σ threshold)
   │         │           │         │
   └────┬────┘           └────┬────┘
        │                     │
   Quality Report         Alert / Flag
        │                     │
   Human Review Queue ←───────┘
```

### Key Capabilities
- **Faithfulness score** — does the answer contradict the source documents?
- **Answer relevancy score** — does the answer actually address the question asked?
- **Context recall** — did the retrieval system find the right chunks?
- **Context precision** — are the retrieved chunks actually relevant?
- **Hallucination demo** — live demonstration with before/after detection
- **Red-teaming panel** — test jailbreaks, out-of-scope queries, adversarial inputs
- **Drift dashboard** — historical metric trends with anomaly flags

### PM Design Decisions
- **Evals as a product feature, not an afterthought** — built in parallel with the main platform. Enterprises ask "how do we know it's accurate?" on day one; the answer has to be ready on day one
- **Show bad outputs, not just good ones** — the hallucination demo deliberately shows a failure case and then shows the detection catching it. This is more trust-building than a demo that only shows perfect outputs
- **RAGAS over custom metrics** — standardised framework means Nestlé/Unilever can compare our scores to industry benchmarks. Custom metrics only matter internally

### Tech Stack
`RAGAS` `Langfuse` `Evidently AI` `LangSmith` `Promptfoo` `Streamlit` `Python`

[![▶ Launch Module](https://img.shields.io/badge/▶_Launch_Module-Live_Demo-FF4B4B?style=flat-square)](https://astra-ai-enterprise-multi-agent-revenue-intelligence-platform.streamlit.app/)

---

## 🏗️ Repo Structure

```
Astra-Multi-Agent-Platform/
├── agents/
│   ├── sdr_agent.py          # SDR lead research + email generation
│   ├── command_centre.py     # Master orchestrator (LangGraph Supervisor)
│   ├── revenue_agent.py      # AE + CFO intelligence agents
│   └── hr_agent.py           # AskHR RAG pipeline
├── rag/
│   ├── embeddings.py         # Document ingestion + vector storage
│   └── retriever.py          # Semantic search + chunk retrieval
├── data/
│   ├── hr_policies/          # HR PDF documents
│   └── sample_pipeline/      # Demo CRM data
├── assets/                   # Images, logos
├── streamlit_app.py          # Main app entry point
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

```bash
git clone https://github.com/karamjeetsingh-ai-pm/Astra-Multi-Agent-Platform
cd Astra-Multi-Agent-Platform
pip install -r requirements.txt

# Add your API keys to .env
cp .env.example .env

streamlit run streamlit_app.py
```

**Required API keys:** `GROQ_API_KEY` · `GEMINI_API_KEY` · `SUPABASE_URL` · `SUPABASE_KEY` · `TAVILY_API_KEY` · `APOLLO_API_KEY`

---

## 👤 Built by

**Karamjeet Singh** · Lead AI Product Manager · [karamjeetsingh.com](https://www.karamjeetsingh.com)

[LinkedIn](https://www.linkedin.com/in/karamjeetsingh-ai-pm/) · [Email](mailto:Karamjeet.6613@gmail.com) · [GitHub](https://github.com/karamjeetsingh-ai-pm)

---

<div align="center">
  <sub>✦ Part of the Astra AI Platform · Built with LangGraph · RAGAS · Groq · Gemini · Supabase · Streamlit</sub>
</div>
