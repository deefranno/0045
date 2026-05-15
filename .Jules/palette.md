## 2025-05-15 - Streamlit 3.12 Compatibility and Progress Visualization
**Learning:** Python 3.12 requires Streamlit >= 1.57.0 to avoid Pillow compilation failures. Using `st.progress` with text labels and gated `st.balloons` via `st.session_state` provides a professional and less intrusive completion experience.
**Action:** Always check the Python version and specify `streamlit>=1.57.0` for 3.12 environments. Use session state to gate terminal animations.
