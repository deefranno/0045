## 2025-05-15 - Streamlit Filter & Animation Polish
**Learning:** Boolean filters in Streamlit are more intuitive when mapped to semantic labels with emojis via `format_func`. Also, terminal animations like `st.balloons()` should be gated by session state to prevent repetitive firing on every interaction.
**Action:** Use `format_func` for status filters and `st.session_state` for one-time animations.

## 2025-05-16 - Streamlit API Modernization
**Learning:** In Streamlit 1.56.0+, `use_container_width=True` is deprecated and generates console noise. The modern replacement is `width="stretch"`.
**Action:** Prefer `width="stretch"` for full-width dataframes and editors to ensure future compatibility.
