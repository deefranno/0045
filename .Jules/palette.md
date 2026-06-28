## 2025-05-15 - Humanizing Boolean State in Streamlit Widgets
**Learning:** Raw boolean values (True/False) in interactive widgets like `st.selectbox` can be confusing for non-technical users. Using the `format_func` parameter allows for mapping these internal states to clear, semantic labels like "Has Issues" or "No Issues" without changing the underlying data logic.
**Action:** Always use `format_func` in Streamlit when mapping technical data types (booleans, enums, IDs) to UI-facing selection components to ensure semantic clarity.
