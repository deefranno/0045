## 2024-05-17 - Semantic Labels and Completion Gating
**Learning:** Using `format_func` in Streamlit selectboxes significantly improves accessibility by replacing technical boolean values with semantic labels like "✅ Annotated" or "⏳ Pending". Additionally, gating celebratory animations (e.g., `st.balloons`) with `st.session_state` prevents cognitive overload from repeating animations on every script rerun.
**Action:** Always prefer `format_func` for boolean or categorical selectboxes and use `st.session_state` to ensure terminal success animations only fire once per completion event.
