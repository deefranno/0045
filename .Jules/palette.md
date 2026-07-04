## 2025-05-15 - Improving semantic clarity in Streamlit filters
**Learning:** Using `format_func` in `st.selectbox` allows mapping technical values (like Booleans) to user-friendly semantic labels ("Has Issues" vs "True"), which improves accessibility and reduces cognitive load.
**Action:** Always use `format_func` or similar mapping mechanisms when internal data values don't directly align with descriptive UI labels.

## 2025-05-15 - Managing one-time visual feedback
**Learning:** Repetitive visual effects like `st.balloons()` on every rerun can become distracting ("balloon fatigue"). Wrapping them in a `st.session_state` check ensures they only fire once per session.
**Action:** Use `st.session_state` to guard one-time delight elements or animations in Streamlit apps.
