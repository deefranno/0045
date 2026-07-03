## 2025-05-14 - Session State for Visual Delights
**Learning:** Streamlit reruns the entire script on every interaction, which can lead to "balloon fatigue" if visual effects like `st.balloons()` are not controlled. Wrapping them in a session state check ensures they only fire once, preserving the "delight" without the annoyance.
**Action:** Always check `st.session_state` before triggering one-time visual animations or effects in Streamlit.
