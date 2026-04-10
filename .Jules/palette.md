## 2026-04-10 - [Streamlit UX Polish and API updates]
**Learning:** In Streamlit v1.56+, `use_container_width=True` is deprecated for `st.dataframe` in favor of `width="stretch"`. Also, boolean filters in selectboxes are more accessible and intuitive when formatted with semantic labels (e.g., "Annotated" vs "Pending") using `format_func`.
**Action:** Use `width="stretch"` for dataframes in modern Streamlit and always provide semantic labels for boolean inputs to improve clarity.
