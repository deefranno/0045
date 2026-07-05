## 2025-05-14 - [Semantic Boolean Labels in Streamlit]
**Learning:** Raw boolean values (True/False) in selectbox filters are not user-friendly. Using `format_func` to map them to descriptive labels like "Has Issues" improves semantic clarity.
**Action:** Always use `format_func` in Streamlit widgets when displaying technical data types like booleans or enums.

## 2025-05-14 - [Balloon Fatigue Prevention]
**Learning:** Streamlit's `st.balloons()` triggers on every script rerun by default, which can be annoying to users. Wrapping it in `st.session_state` ensures it only fires once per session.
**Action:** Wrap one-time visual effects in a session state check to prevent repetitive triggers during user interactions.
