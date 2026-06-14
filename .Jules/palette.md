## 2026-06-14 - Preventing redundant animations in Streamlit
**Learning:** Streamlit's execution model causes the entire script to rerun on every interaction. One-time "delight" features like `st.balloons()` become intrusive "balloon fatigue" if they fire repeatedly during a user's session.
**Action:** Always wrap one-time visual effects or heavy initialization logic in a `st.session_state` check to ensure they only occur once per session.
