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
    st.caption("Orchestrate multiple AI agents on complex enterprise tasks")
    st.divider()
    st.info("🚧 Building in Step 4 — Multi-Agent Orchestration")

elif page == "🤖 SDR Agent":
    st.markdown("## 🤖 Autonomous SDR Agent")
    st.caption("AI-powered lead finding, research, personalization and outreach")
    st.divider()
    st.info("🚧 Building in Step 5 — SDR Agent")

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