## 2026-05-01 - Progress Visualization and Filter Polish
**Learning:** In Streamlit apps, `st.progress` provides a much clearer sense of task completion than a numerical metric alone. Using `format_func` in selectboxes to map technical values (like Booleans) to semantic labels (with emojis) significantly improves cognitive speed for users.
**Action:** Always prefer `st.progress` for terminal workflows and use `format_func` to provide semantic context to data-driven selectboxes.
