import streamlit as st
import numpy as np
import pandas as pd

# --- Page setup ---
st.set_page_config(page_title="Law of Large Numbers", layout="centered")
st.title("Law of Large Numbers – Bernoulli Simulation")

st.markdown(
    """
    This app simulates Bernoulli trials for different sample sizes  
    and shows how the empirical frequency converges to the probability *p*.
    """
)

# --- User input ---
p = st.slider("Choose probability p", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
seed = st.number_input("Random seed (optional)", value=42, step=1)
include_big_n = st.checkbox("Include n = 10,000,000 (may take a while)", value=False)

# Sample sizes
n_values = [10, 50, 100, 1000] + ([10_000_000] if include_big_n else [])

run = st.button("Run simulation")

# --- Computation ---
if run:
    rng = np.random.default_rng(int(seed))

    rows = []
    for n in n_values:
        successes = rng.binomial(n=n, p=p)
        result = successes / n
        abs_diff = abs(result - p)
        rows.append({"n": n, "result": result, "|result - p|": abs_diff})

    df = pd.DataFrame(rows)

    # --- Results ---
    st.subheader("Results")
    st.dataframe(
        df.style.format({"result": "{:.4f}", "|result - p|": "{:.4f}"}),
        use_container_width=True,
    )

    # --- Visualization ---
    st.subheader("Visualization")
    st.line_chart(df.set_index("n")[["result"]], x_label="n", y_label="result")
    st.line_chart(df.set_index("n")[["|result - p|"]], x_label="n", y_label="|result - p|")

    st.caption(
        "The theoretical value is p. As n increases, the empirical frequency "
        "tends to get closer to p, illustrating the law of large numbers."
    )

else:
    st.info("Set parameters and click **Run simulation**.")
