import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# --- Page setup ---
st.set_page_config(page_title="Law of Large Numbers (log-scale charts)", layout="centered")
st.title("Law of Large Numbers – Bernoulli Simulation (log-scale)")

st.markdown(
    """
    This app simulates Bernoulli trials for several sample sizes and shows:
    1) the empirical frequency (*result*), and
    2) the absolute deviation from *p* (|result − p|).

    The x‑axis uses a **logarithmic scale (base 10)** so equal spacing represents equal
    multiplicative steps in *n* (10 → 100 → 1000 → …).
    Each run generates new random results (no fixed seed).
    """
)

# --- User input ---
p = st.slider("Choose probability p", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
include_big_n = st.checkbox("Include n = 10,000,000 (may take a while)", value=False)

# Sample sizes
n_values = [10, 50, 100, 1000] + ([10_000_000] if include_big_n else [])

run = st.button("Run simulation")

# --- Computation ---
if run:
    rng = np.random.default_rng()  # Always random – no fixed seed

    rows = []
    for n in n_values:
        successes = rng.binomial(n=n, p=p)
        result = successes / n
        abs_diff = abs(result - p)
        rows.append({"n": n, "result": result, "|result - p|": abs_diff})

    df = pd.DataFrame(rows)

    # --- Results table (4 decimals) ---
    st.subheader("Results")
    st.dataframe(
        df.style.format({"result": "{:.4f}", "|result - p|": "{:.4f}"}),
        use_container_width=True,
    )

    # --- Charts with log-scale x-axis (base 10) ---
    st.subheader("Visualization (log-scale x-axis)")

    # Chart 1: result vs n
    chart1 = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("n:Q", scale=alt.Scale(type="log"), title="n (log scale, base 10)"),
            y=alt.Y("result:Q", title="result"),
            tooltip=[alt.Tooltip("n:Q"), alt.Tooltip("result:Q", format=".4f")],
        )
        .properties(title="Empirical frequency vs. sample size")
    )

    # Add horizontal reference line at y = p
    rule = alt.Chart(pd.DataFrame({"y": [p]})).mark_rule(strokeDash=[6,4]).encode(y="y:Q")

    st.altair_chart(chart1 + rule, use_container_width=True)

    # Chart 2: |result - p| vs n
    chart2 = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("n:Q", scale=alt.Scale(type="log"), title="n (log scale, base 10)"),
            y=alt.Y("|result - p|:Q", title="|result - p|"),
            tooltip=[alt.Tooltip("n:Q"), alt.Tooltip("|result - p|:Q", format=".4f")],
        )
        .properties(title="Absolute difference vs. sample size")
    )

    st.altair_chart(chart2, use_container_width=True)

    st.caption(
        "As n grows multiplicatively (×10), the empirical frequency typically approaches p, "
        "and the absolute deviation tends to decrease. The log-scale x‑axis makes these "
        "orders of magnitude visually comparable."
    )
else:
    st.info("Set parameters and click **Run simulation**.")
