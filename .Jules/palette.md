## 2026-05-25 - Robustness in Streamlit Dynamic Filters
**Learning:** `st.selectbox` will crash with a `StreamlitAPIException` if the `options` list is empty, even if the widget is set to `disabled=True`. This is a common pitfall when using dynamic filters based on data editor states.
**Action:** Always provide a fallback option (e.g., `["None"]`) and ensure the `options` parameter is never an empty collection.

## 2026-05-25 - Streamlit Dataframe Sizing API
**Learning:** Contrary to some documentation or LLM suggestions, `st.dataframe(..., width="stretch")` can be an invalid API call in modern Streamlit versions, leading to a crash.
**Action:** Use `use_container_width=True` to ensure dataframes and editors expand to the full width of their container reliably.
