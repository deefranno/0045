## 2026-04-18 - Semantic Labeling and Filter Feedback in Data Annotation
**Learning:** Raw booleans in filters lack semantic clarity for annotators. Providing immediate feedback when a filtered view is empty prevents user confusion and confirms the app is still responsive.
**Action:** Use `format_func` in `st.selectbox` for boolean filters and implement `st.info` or `st.warning` for empty filtered states.
