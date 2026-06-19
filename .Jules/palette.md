## 2026-06-19 - [Streamlit Micro-UX & Accessibility]
**Learning:** In Streamlit, visual effects like `st.balloons()` can cause "balloon fatigue" if fired on every rerun. Additionally, displaying raw boolean values (True/False) in selection UI is poor UX; using `format_func` to map them to descriptive labels like "Annotated" improves clarity and accessibility.
**Action:** Always wrap one-time visual effects in a `st.session_state` check and use `format_func` for human-readable labels in selectboxes and other selection components.
