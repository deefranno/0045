# Palette's UX Journal

## 2025-05-14 - Gating Celebratory Animations
**Learning:** In Streamlit, calling `st.balloons()` at the top of the script causes it to trigger on every rerun (e.g., when a user interacts with a widget), which can be distracting and block content.
**Action:** Relocate celebratory animations to the end of the script and use `st.session_state` to ensure they only trigger once per session.
