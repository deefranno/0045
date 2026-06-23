## 2026-06-23 - [Improved selectbox label clarity]
**Learning:** Raw boolean values (`True`/`False`) in Streamlit filters are unintuitive for non-technical users. Using `format_func` in `st.selectbox` allows mapping these technical values to human-readable labels (e.g., "Has Issues") without changing the underlying data logic.
**Action:** Always use `format_func` when displaying boolean or internal enum values in Streamlit widgets to ensure the UI remains semantic and accessible.
