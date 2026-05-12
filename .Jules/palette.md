## 2026-05-12 - Gated Terminal Animations in Streamlit
**Learning:** Celebratory animations like `st.balloons()` can be jarring if they fire on every script rerun (common in Streamlit). Using `st.session_state` to gate these animations ensures they only trigger once upon reaching a terminal success state, significantly reducing cognitive load.
**Action:** Always wrap terminal feedback animations in a session state check and provide a mechanism to reset the state if the progress falls below the completion threshold.
