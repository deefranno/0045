## 2025-05-14 - Streamlit UX Polish: One-time Effects and Semantic Labels
**Learning:** Streamlit's "rerun-on-interaction" model means visual celebrations like `st.balloons()` can quickly become annoying if not guarded by session state. Additionally, displaying raw boolean values in UI filters is confusing for users; mapping them to semantic labels (e.g., "Has Issues") significantly improves clarity and accessibility.
**Action:** Guard one-time visual effects with `st.session_state` and always use `format_func` to provide human-readable labels for technical data in Streamlit widgets.
