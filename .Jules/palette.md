## 2026-07-01 - Preventing visual fatigue in Streamlit
**Learning:** Streamlit reruns the entire script on every user interaction. One-time visual effects like `st.balloons()` can become annoying if they trigger on every rerun. Using `st.session_state` to guard these effects ensures they only provide delight without becoming a nuisance.
**Action:** Always wrap one-time visual interactions in a session state check in Streamlit applications.

## 2026-07-01 - Semantic labels for boolean states
**Learning:** Raw boolean values (`True`/`False`) in UI elements like selectboxes are not user-friendly. Using `format_func` in `st.selectbox` allows mapping these technical states to descriptive, semantic labels (e.g., "Has Issues") without changing the underlying data structure.
**Action:** Use `format_func` to provide human-readable labels for technical data values in selectboxes and other selection widgets.
