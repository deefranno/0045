# Palette's Journal - Critical UX Learnings

## 2025-05-15 - Streamlit Compatibility and Stability
**Learning:** Python 3.12 compatibility for Streamlit requires version 1.57.0 or higher to avoid Pillow dependency compilation failures in certain environments. Additionally, `st.selectbox` will crash with a `StreamlitAPIException` if `options` is empty.
**Action:** Always verify Streamlit versions in `requirements.txt` for Python 3.12+ projects and provide fallbacks/disabled states for selectboxes with dynamic options.

## 2025-05-15 - Feedback and Delight Patterns
**Learning:** Using `st.session_state` to gate terminal success animations (like `st.balloons`) ensures they only trigger once per session and don't re-fire on every script rerun, preventing UX fatigue.
**Action:** Implement state-gated animations for completion events.
