## 2026-04-14 - [Session State for Animations]
**Learning:** Streamlit animations like `st.balloons()` trigger on every rerun, which can be disruptive. Gating them with `st.session_state` ensures they only fire once per session.
**Action:** Always use a session state flag to control celebratory or one-time UI events in Streamlit.

## 2026-04-14 - [Readable Labels for Booleans]
**Learning:** Raw boolean values (True/False) in UI filters lack context. Using `format_func` in `st.selectbox` allows mapping these to domain-specific labels like "Annotated" and "Pending".
**Action:** Use `format_func` for all boolean-driven selection widgets to improve clarity.
