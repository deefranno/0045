## 2026-05-04 - Semantic Labels for Boolean Filters
**Learning:** Using raw boolean values (True/False) in UI filters is confusing for end-users. Semantic labels with emojis (e.g., "✅ Issues Found") significantly improve scannability and clarity.
**Action:** Always use `format_func` in Streamlit selectboxes when dealing with boolean or coded values to provide human-readable descriptions.

## 2026-05-04 - Defensive Empty States in Dashboards
**Learning:** Filtered dataframes that return empty sets can look like app errors or "broken" UI if not handled gracefully.
**Action:** Implement `st.info` or `st.warning` fallback messages when a filtered result set is empty to guide the user on how to resolve it (e.g., "Adjust filters to view data").
