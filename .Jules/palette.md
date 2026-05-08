
## 2025-05-14 - Semantic Distinction in Evaluation Tools
**Learning:** In data annotation/evaluation apps, overloading a single boolean column to represent both "Completion Status" and "Negative Finding" (e.g., 'Issue') creates confusing UX and broken metrics. Completion should always be explicitly tracked (e.g., 'Reviewed') separately from the findings themselves.
**Action:** Always provide a dedicated 'Reviewed/Verified' status column for progress tracking, distinct from 'Issue/Error' finding columns.

## 2025-05-14 - Streamlit 1.57+ Container Width Deprecation
**Learning:** The long-standing 'use_container_width=True' parameter in Streamlit components like 'st.data_editor' and 'st.dataframe' is being deprecated in favor of more explicit 'width="stretch"' or 'width="content"' options.
**Action:** Prefer 'width="stretch"' for full-width components in modern Streamlit applications to ensure forward compatibility and clearer layout intent.
