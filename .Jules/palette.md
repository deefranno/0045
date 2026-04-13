## 2025-05-14 - Gating terminal success animations
**Learning:** In Streamlit apps, celebratory animations like `st.balloons()` should be gated with `st.session_state` to prevent them from re-firing on every subsequent script rerun (e.g., when the user changes a filter after completion).
**Action:** Use a boolean flag in `st.session_state` to track if the terminal success state has already been celebrated.
