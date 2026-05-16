## 2026-05-16 - [Streamlit Selectbox Crash Prevention]
**Learning:** In Streamlit, `st.selectbox` (and other selection components) will raise a `StreamlitAPIException` if the `options` list is empty. This often happens in dynamic filtering scenarios where a subset of data might have no valid categories.
**Action:** Always ensure `options` is non-empty by providing a fallback (e.g., `["None"]`) or gating the component call. Combining this with `disabled=len(options) == 0` provides a clean UX that prevents application crashes.
