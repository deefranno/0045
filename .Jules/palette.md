## 2026-06-29 - Preventing Balloon Fatigue in Streamlit
**Learning:** Because Streamlit reruns the entire script on every interaction, visual effects like `st.balloons()` will trigger repeatedly, leading to a distracting user experience.
**Action:** Always wrap one-time visual effects in a `st.session_state` check to ensure they only fire once per session.

## 2026-06-29 - Human-Friendly Boolean Labels
**Learning:** Displaying raw `True`/`False` values in filters or metrics can be confusing for users as it lacks technical context.
**Action:** Use the `format_func` parameter in `st.selectbox` and descriptive labels in `st.metric` to map internal state to domain-specific terminology (e.g., 'Has Issues' instead of 'True').
