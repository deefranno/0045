## 2025-05-15 - Streamlit Micro-UX & Deprecations
**Learning:** Streamlit 1.57.0 introduced 'width="stretch"' as the preferred replacement for 'use_container_width'. Additionally, terminal celebratory animations like 'st.balloons()' should be gated by 'st.session_state' to prevent them from re-firing on every user interaction (script rerun), which can be intrusive.
**Action:** Use 'width="stretch"' for full-width components in newer Streamlit versions and always implement a state-check before triggering one-time visual effects.
