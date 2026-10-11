import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from data import SECTORS
from ai_debate import SCENARIOS, run_debate, apply_adjustments

st.title("The AI Boardroom")
sector = st.selectbox("Pick a sector", list(SECTORS.keys()))


def compute_scores(uc):
    return uc["value"] * 2, uc["deploy"] + uc["trust"]


def make_matrix(use_cases):
    points = [compute_scores(uc) for uc in use_cases]
    fig = go.Figure(go.Scatter(
        x=[p[1] for p in points], y=[p[0] for p in points],
        text=[str(i + 1) for i in range(len(use_cases))],
        customdata=[uc["name"] for uc in use_cases],
        hovertemplate="%{customdata}<br>Feasibility: %{x}<br>Impact: %{y}<extra></extra>",
        mode="markers+text", textposition="middle center",
        textfont=dict(color="white", size=14), marker=dict(size=34, opacity=0.85)))
    fig.add_vline(x=5.5, line_dash="dot")
    fig.add_hline(y=5.5, line_dash="dot")
    fig.update_layout(xaxis=dict(title="Feasibility (how easy)", range=[0, 11]),
                      yaxis=dict(title="Impact (how valuable)", range=[0, 11]), height=520)
    return fig


st.subheader("The Boardroom")
cols = st.columns(len(SCENARIOS))
clicked = None
for col, name in zip(cols, SCENARIOS):
    if col.button(name):
        clicked = name

left, right = st.columns([3, 2])
chart_slot = left.empty()
with right:
    st.markdown("**The debate**")
    chat_slot = st.container()

if clicked:
    with st.spinner("The board is assembling..."):
        result, source, error = run_debate(sector, clicked)
    st.session_state["debate"] = {"sector": sector, "scenario": clicked,
                                  "result": result, "source": source, "error": error}
    animate = True
else:
    animate = False

saved = st.session_state.get("debate")

if saved and saved["sector"] == sector:
    result = saved["result"]
    if saved["source"] == "demo":
        st.warning("DEMO MODE: this is canned text, not a live AI answer. " + (saved["error"] or ""))
    st.markdown("**Scenario:** " + saved["scenario"])

    turns = result["turns"]
    for i, turn in enumerate(turns, start=1):
        with chat_slot.chat_message("assistant"):
            st.markdown("**" + turn["agent"] + ":** " + turn["message"])
            for a in turn["adjustments"]:
                st.caption("Use case " + str(a["id"]) + ", " + a["factor"] + " " + format(a["delta"], "+d") + ": " + a.get("reason", ""))
        chart_slot.plotly_chart(make_matrix(apply_adjustments(sector, result, i)),
                                key="turn_" + str(i), width="stretch")
        if animate:
            time.sleep(1.6)

    final = apply_adjustments(sector, result, len(turns))
    kill = {k["id"]: k["line"] for k in result["verdict"].get("kill_criteria", [])}
    with chat_slot.chat_message("assistant"):
        st.markdown("**Verdict:** " + result["verdict"]["summary"])

    rows = []
    for i, uc in enumerate(final, start=1):
        impact, feas = compute_scores(uc)
        rows.append({"#": i, "Name": uc["name"], "Score": round((impact + feas) / 2, 1),
                     "Kill criteria": kill.get(i, "")})
    table = pd.DataFrame(rows).sort_values("Score", ascending=False)
    st.subheader("Final roadmap")
    st.dataframe(table, hide_index=True)
else:
    chart_slot.plotly_chart(make_matrix(SECTORS[sector]), key="start", width="stretch")
    st.info("Press a scenario button to start the boardroom.")

st.subheader("Score Breakdown")
for i, uc in enumerate(SECTORS[sector], start=1):
    with st.expander(str(i) + ". " + uc["name"]):
        st.caption(uc["why"])
        st.caption("Source: " + uc["source"] + " | Confidence: " + uc["confidence"])