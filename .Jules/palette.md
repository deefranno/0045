# Palette's UX Journal

## 2025-05-22 - Preventing Balloon Fatigue
**Learning:** In Streamlit applications, every user interaction triggers a full script rerun. Visual effects like `st.balloons()` that are placed at the root level will execute on every click, leading to "balloon fatigue" and distracting the user from their task.
**Action:** Wrap one-time visual celebrations in a `st.session_state` check to ensure they only trigger once per session.
