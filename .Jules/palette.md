# Palette's Journal - Critical UX Learnings

## 2026-06-21 - Improving Boolean Filter Clarity
**Learning:** Raw boolean values (True/False) in UI components like selectboxes can be ambiguous and less intuitive than descriptive labels. Mapping internal state (True/False) to domain-specific labels (e.g., "Has Issue" vs "No Issue") improves semantic clarity and accessibility.
**Action:** Use `format_func` in Streamlit `st.selectbox` (or equivalent in other frameworks) to map internal data values to user-friendly, descriptive labels.
