import streamlit as st
import json

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Multi-Agent Newsroom",
    layout="wide"
)

st.title("🗞️ Multi-Agent Newsroom Dashboard")

# -------------------------
# Load Logs
# -------------------------
try:
    with open("logs.json", "r") as f:
        logs = json.load(f)
except:
    st.error("logs.json not found")
    st.stop()

# Separate logs
agent_logs = [l for l in logs if "agent_name" in l]
state_logs = [l for l in logs if l.get("type") == "STATE_TRANSITION"]

# -------------------------
# Helper Functions
# -------------------------
def format_verdict(verdict):
    if verdict == "PASS":
        return f"🟢 {verdict}"
    elif verdict == "WARN":
        return f"🟡 {verdict}"
    elif verdict == "FAIL":
        return f"🔴 {verdict}"
    return verdict

# -------------------------
# Layout
# -------------------------
col1, col2 = st.columns([1, 3])

# =========================
# Agent Panel
# =========================
with col1:
    st.subheader("🧠 Agents")

    agents = ["REPORTER", "FACT_CHECKER", "EDITOR", "PUBLISHER"]
    last_agent = agent_logs[-1]["agent_name"] if agent_logs else None

    for agent in agents:
        if agent == last_agent:
            st.markdown(f"🔄 **{agent}**")
        else:
            st.markdown(f"⬜ {agent}")

# =========================
# State + Interaction Panel
# =========================
with col2:

    # ---- State Panel ----
    st.subheader("🔄 Current State")

    if state_logs:
        current_state = state_logs[-1]["to"]
        st.success(current_state)

        with st.expander("View State Transitions"):
            for s in state_logs:
                st.text(f"{s['from']} → {s['to']}")

    # ---- Interaction Panel ----
    st.subheader("💬 Agent Interactions")

    for log in agent_logs:
        agent = log["agent_name"]
        output = log["output"]

        with st.container():
            st.markdown(f"### {agent}")
            
            # Reporter
            if "headline" in output:
                st.write(f"**Headline:** {output['headline']}")
                st.write(f"**Body:** {output.get('body', '')}")

            # Fact Checker
            if "score" in output:
                verdict = format_verdict(output.get("verdict", ""))
                st.write(f"**Score:** {output['score']}  |  **Verdict:** {verdict}")

            # Editor
            if "decision" in output:
                st.write(f"**Decision:** {output['decision']}")

            # Publisher
            if "published" in output:
                st.write(f"**Published:** {output['published']}")

            st.markdown("---")

# =========================
# Metrics Panel
# =========================
st.subheader("📊 Metrics")

scores = [l["output"]["score"] for l in agent_logs if "score" in l["output"]]
verdicts = [l["output"].get("verdict") for l in agent_logs if "verdict" in l["output"]]
decisions = [l["output"].get("decision") for l in agent_logs if "decision" in l["output"]]

col3, col4, col5 = st.columns(3)

# Average Score
with col3:
    if scores:
        avg_score = sum(scores) / len(scores)
        st.metric("Avg Credibility Score", round(avg_score, 2))
    else:
        st.metric("Avg Credibility Score", "N/A")

# Detection Rate (WARN + FAIL)
with col4:
    flagged = len([v for v in verdicts if v in ["WARN", "FAIL"]])
    total = len(verdicts)
    rate = (flagged / total * 100) if total > 0 else 0
    st.metric("Misinformation Detection", f"{round(rate, 1)}%")

# Rejection Rate
with col5:
    rejected = len([d for d in decisions if d == "REJECTED"])
    total_d = len(decisions)
    rate_r = (rejected / total_d * 100) if total_d > 0 else 0
    st.metric("Editor Rejection Rate", f"{round(rate_r, 1)}%")