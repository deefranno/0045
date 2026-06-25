## 2026-06-25 - Enhancing Streamlit Annotation Interfaces
**Learning:** In Streamlit-based data evaluation tools, raw technical values (like booleans) in filters create friction. Using `format_func` in `st.selectbox` to provide semantic labels ("Has Issues") and `help` tooltips for metrics significantly lowers the cognitive load for annotators without adding interface clutter.
**Action:** Always map internal data states to descriptive user-facing labels and leverage built-in tooltip parameters for metrics and inputs in Streamlit apps.
