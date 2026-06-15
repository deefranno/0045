## 2025-05-22 - Preventing Balloon Fatigue
**Learning:** In Streamlit, visual effects like `st.balloons()` trigger on every script rerun (e.g., when a user interacts with a widget). This causes "balloon fatigue" where the animation becomes annoying rather than delightful.
**Action:** Always wrap one-time visual celebrations in a `st.session_state` check to ensure they only run once per session.
