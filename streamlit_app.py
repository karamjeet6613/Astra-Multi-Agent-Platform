import streamlit as st
import base64
import sys
import os
from dotenv import load_dotenv

load_dotenv()

for key in ["GEMINI_API_KEY", "GROQ_API_KEY", "TAVILY_API_KEY", "SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_KEY"]:
    try:
        if key in st.secrets:
            os.environ[key] = str(st.secrets[key]).strip()
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Astra — Multi-Agent Platform",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_svg_logo(size: int = 36) -> str:
    svg_path = os.path.join(os.path.dirname(__file__), "assets", "astra-ai-icon.svg")
    with open(svg_path, "r") as f:
        svg = f.read()
    b64 = base64.b64encode(svg.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{size}" height="{size}" style="vertical-align:middle; margin-right:8px;">'

with st.sidebar:
    st.markdown(f'{get_svg_logo(40)} <span style="font-size:1.3rem;font-weight:700;">Astra</span>', unsafe_allow_html=True)
    st.caption("Multi-Agent Intelligence Platform")
    st.divider()
    st.markdown("**Navigation**")
    page = st.radio("Navigation", [
        "🏠 Home",
        "🧠 Command Center",
        "🤖 SDR Agent",
        "💰 Revenue Intelligence",
        "❓ AskHR",
        "🔬 Evals",
    ], label_visibility="collapsed")
    st.divider()
    st.caption("NexaCore Technologies Inc.")
    st.caption("Demo 3 — Multi-Agent Autonomy")

# ── Pages ──────────────────────────────────────

if page == "🏠 Home":
    st.markdown(f'## {get_svg_logo(32)} Welcome to Astra', unsafe_allow_html=True)
    st.markdown("#### Multi-Agent AI Platform — Demo 3")
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🧠 Command Center**\n\nOrchestrate multiple AI agents on complex tasks")
    with col2:
        st.success("**🤖 SDR Agent**\n\nAutonomous lead finding, research and outreach")
    with col3:
        st.warning("**💰 Revenue Intelligence**\n\nAE pipeline view + CFO analytics toggle")
    col4, col5 = st.columns(2)
    with col4:
        st.error("**❓ AskHR**\n\nRAG-powered HR policy assistant")
    with col5:
        st.info("**🔬 Evals**\n\nRAGAS scores + Hallucination demo")

elif page == "🧠 Command Center":
    st.markdown("## 🧠 Command Center")
    st.caption("Give Astra a complex task — watch multiple agents collaborate in real-time")
    st.divider()

    # Sample tasks
    st.markdown("**💡 Try these multi-agent tasks:**")
    sample_tasks = [
        "Why is APAC underperforming and what should HR do to retain top sales talent there?",
        "Analyze our Q4 revenue and suggest a hiring plan for next quarter",
        "Find recent AI trends in enterprise sales and suggest how we can use them",
        "Which sales reps need coaching and what HR resources are available for them?",
        "Summarize our pipeline health and recommend budget reallocation",
    ]
    cols = st.columns(2)
    for i, task in enumerate(sample_tasks):
        with cols[i % 2]:
            if st.button(task, key=f"cmd_{i}", use_container_width=True):
                st.session_state.cmd_task = task

    st.divider()

    if "cmd_messages" not in st.session_state:
        st.session_state.cmd_messages = []
    if "cmd_task" not in st.session_state:
        st.session_state.cmd_task = ""

    # Display history
    for msg in st.session_state.cmd_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("plan"):
                with st.expander("🗺️ Agent Plan"):
                    for agent, subtask in msg["plan"]:
                        st.caption(f"• **{agent.upper()}**: {subtask}")

    task = st.chat_input("Give Astra a complex task...") or st.session_state.cmd_task
    if st.session_state.cmd_task:
        st.session_state.cmd_task = ""

    if task:
        st.session_state.cmd_messages.append({"role": "user", "content": task})
        with st.chat_message("user"):
            st.write(task)

        with st.chat_message("assistant"):
            st.markdown("**🧠 Astra is orchestrating...**")
            live_container = st.container()
            with st.spinner("Agents working..."):
                try:
                    from agents.orchestrator import orchestrate
                    result = orchestrate(task, stream_container=live_container)
                    st.divider()
                    st.markdown("**📋 Final Response:**")
                    st.write(result["final"])
                    st.session_state.cmd_messages.append({
                        "role": "assistant",
                        "content": result["final"],
                        "plan": result["plan"]
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "🤖 SDR Agent":
    st.markdown("## 🤖 Autonomous SDR Agent")
    st.caption("AI finds leads, researches companies, writes personalized emails — you approve before sending")
    st.divider()

    # Campaign Setup
    col1, col2 = st.columns([3, 1])
    with col1:
        criteria = st.text_input(
            "Target criteria",
            placeholder="e.g. SaaS companies in London, 50-200 employees, hiring sales roles",
            value="B2B SaaS companies in UK, 50-200 employees"
        )
    with col2:
        num_leads = st.selectbox("Leads", [3, 5, 8, 10], index=1)

    if "sdr_pipeline" not in st.session_state:
        st.session_state.sdr_pipeline = []
    if "sdr_running" not in st.session_state:
        st.session_state.sdr_running = False

    col_run, col_clear = st.columns([1, 4])
    with col_run:
        run_btn = st.button("🚀 Run Campaign", type="primary", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear Pipeline", use_container_width=True):
            st.session_state.sdr_pipeline = []
            st.rerun()

    if run_btn and criteria:
        st.session_state.sdr_pipeline = []
        progress_container = st.container()

        with progress_container:
            st.markdown("**⚡ SDR Agent Running...**")
            status_box = st.empty()
            progress_bar = st.progress(0)

        steps_done = [0]

        def update_progress(step, msg):
            status_box.info(msg)
            steps_done[0] += 1
            progress_bar.progress(min(steps_done[0] / (num_leads * 3 + 2), 1.0))

        try:
            from agents.sdr_agent import run_sdr_campaign
            pipeline = run_sdr_campaign(criteria, num_leads, callback=update_progress)
            st.session_state.sdr_pipeline = pipeline
            progress_bar.progress(1.0)
            status_box.success(f"✅ Campaign complete! {len(pipeline)} leads ready for review")
        except Exception as e:
            st.error(f"Error: {e}")

    # Display Pipeline
    if st.session_state.sdr_pipeline:
        st.divider()
        st.markdown(f"### 📋 Pipeline — {len(st.session_state.sdr_pipeline)} Leads")

        # Summary metrics
        pipeline = st.session_state.sdr_pipeline
        hot = sum(1 for l in pipeline if "Hot" in l["score"])
        warm = sum(1 for l in pipeline if "Warm" in l["score"])
        cold = sum(1 for l in pipeline if "Cold" in l["score"])
        approved = sum(1 for l in pipeline if l.get("approved"))

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🔥 Hot Leads", hot)
        m2.metric("🟡 Warm Leads", warm)
        m3.metric("❄️ Cold Leads", cold)
        m4.metric("✅ Approved", approved)

        st.divider()

        # Lead cards
        for i, lead in enumerate(st.session_state.sdr_pipeline):
            with st.expander(f"{lead['score']} {lead['company']} | ICP: {lead['icp_score']}/10 | {lead['industry']} | {lead['status']}", expanded=i==0):
                col_info, col_email = st.columns([1, 2])

                with col_info:
                    st.markdown("**Company Intel**")
                    st.caption(f"🌐 {lead['url']}")
                    st.caption(f"👤 Target: {lead['decision_maker']}")
                    st.caption(f"🏢 Size: {lead['size']}")
                    st.caption(f"📊 ICP Score: {lead['icp_score']}/10")
                    st.caption(f"💡 {lead['icp_reason']}")
                    st.markdown("**Pain Points**")
                    for pp in lead["pain_points"]:
                        st.caption(f"• {pp}")
                    st.markdown("**Buying Signals**")
                    for bs in lead["buying_signals"]:
                        st.caption(f"• {bs}")

                with col_email:
                    st.markdown("**✉️ Personalized Email**")
                    st.info(f"**Subject:** {lead['email'].get('subject', '')}")
                    st.text_area("Email body", lead['email'].get('body', ''), height=180, key=f"email_{i}")

                    with st.expander("📅 Follow-up Sequence"):
                        for j, fu in enumerate(lead.get("followups", [])):
                            st.caption(f"**Day {[3,7][j]} Follow-up**")
                            st.caption(f"Subject: {fu.get('subject', '')}")
                            st.caption(fu.get('body', '')[:200] + "...")

                # Human-in-the-Loop approval
                st.divider()
                col_approve, col_reject, col_edit = st.columns(3)
                with col_approve:
                    if st.button(f"✅ Approve & Queue", key=f"approve_{i}", use_container_width=True):
                        st.session_state.sdr_pipeline[i]["approved"] = True
                        st.session_state.sdr_pipeline[i]["status"] = "Approved ✅"
                        st.rerun()
                with col_reject:
                    if st.button(f"❌ Reject", key=f"reject_{i}", use_container_width=True):
                        st.session_state.sdr_pipeline[i]["status"] = "Rejected ❌"
                        st.rerun()
                with col_edit:
                    if st.button(f"✏️ Needs Edit", key=f"edit_{i}", use_container_width=True):
                        st.session_state.sdr_pipeline[i]["status"] = "Needs Edit ✏️"
                        st.rerun()

elif page == "💰 Revenue Intelligence":
    st.markdown("## 💰 Revenue Intelligence")
    st.caption("AE pipeline view + CFO analytics — toggle between perspectives")
    st.divider()
    st.info("🚧 Building in Step 6 — Revenue Intelligence")

elif page == "❓ AskHR":
    st.markdown("## ❓ AskHR")
    st.caption("Ask any HR question — answers from NexaCore HR policy documents")
    st.divider()

    st.markdown("**💡 Try asking:**")
    cols = st.columns(3)
    sample_questions = [
        "How many PTO days do I get?",
        "What is the maternity leave policy?",
        "How does the bonus structure work?",
        "What is the notice period?",
        "How do I apply for sick leave?",
        "What is the 401k matching policy?",
    ]
    for i, q in enumerate(sample_questions):
        with cols[i % 3]:
            if st.button(q, key=f"sq_{i}", use_container_width=True):
                st.session_state.hr_question = q

    st.divider()

    if "hr_messages" not in st.session_state:
        st.session_state.hr_messages = []
    if "hr_question" not in st.session_state:
        st.session_state.hr_question = ""

    for msg in st.session_state.hr_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander("📄 Sources"):
                    for src in msg["sources"]:
                        st.caption(f"• {src}")

    question = st.chat_input("Ask an HR question...") or st.session_state.hr_question
    if st.session_state.hr_question:
        st.session_state.hr_question = ""

    if question:
        st.session_state.hr_messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Searching HR policies..."):
                try:
                    from agents.ask_hr import ask_hr
                    result = ask_hr(question)
                    st.write(result["answer"])
                    if result["sources"]:
                        with st.expander(f"📄 Sources ({result['docs_found']} documents found)"):
                            for src in result["sources"]:
                                st.caption(f"• {src}")
                    st.session_state.hr_messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"]
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "🔬 Evals":
    st.markdown("## 🔬 RAGAS Evals + Hallucination Demo")
    st.caption("Live evaluation scores + RAG vs No-RAG comparison")
    st.divider()
    st.info("🚧 Building in Step 7 — Evals")