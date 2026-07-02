## 2026-07-02 - Enhancing Streamlit Feedback and Data Clarity
**Learning:** In Streamlit, ephemeral visual effects like `st.balloons()` rerun on every interaction, leading to "balloon fatigue." Additionally, mapping raw internal states (like booleans) to semantic labels in filters and metrics significantly improves user comprehension.
**Action:** Always wrap one-time visual effects in a `st.session_state` check and use `format_func` in selectboxes to provide descriptive labels for technical values.
