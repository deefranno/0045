## 2025-05-14 - [Streamlit UX Micro-patterns]
**Learning:** In Streamlit, visual effects like `st.balloons()` should be guarded by `st.session_state` to prevent repetitive triggers on every widget interaction. Additionally, mapping internal boolean states to semantic labels via `format_func` in `st.selectbox` significantly improves accessibility and clarity for non-technical users.
**Action:** Always wrap one-time visual effects in session state checks and use `format_func` to provide human-readable labels for abstract data types in selectors.
