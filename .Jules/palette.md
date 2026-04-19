# Palette's UX Journal

## 2026-04-19 - [Initial Setup]
**Learning:** Streamlit apps often fire celebratory animations like `st.balloons()` on every rerun, which can be distracting. They should be gated by session state and reserved for terminal success.
**Action:** Use `st.session_state` to ensure animations only play once when a specific condition (like 100% progress) is met.
