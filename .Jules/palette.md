## 2026-05-14 - Streamlit UX Enhancements

**Learning:** Gating terminal success animations (like `st.balloons`) with `st.session_state` is essential for Streamlit apps to avoid overwhelming the user on every script rerun. Additionally, using `disabled` on dependent selectboxes when no options are available prevents confusing empty interactions. In Streamlit 1.57.0+, `width="stretch"` is the preferred way to handle container width for dataframes.

**Action:** Always use a session state flag for one-time animations and disable dependent inputs when their data source is empty. Use `width="stretch"` for full-width dataframes in modern Streamlit.
