## 2025-05-14 - Prevent Animation Fatigue in Streamlit
**Learning:** st.balloons() fires on every script rerun in Streamlit, which happens with every user interaction. This leads to "animation fatigue" and a frustrating UX.
**Action:** Always gate terminal success animations like st.balloons() behind a session state check (e.g., if 'balloons_fired' not in st.session_state) to ensure they only trigger once per session.

## 2025-05-14 - Semantic Labels for Boolean Filters
**Learning:** Raw boolean values (True/False) in UI filters are not user-friendly or accessible.
**Action:** Use the 'format_func' parameter in st.selectbox to provide semantic labels and include emoji prefixes (e.g., '⚠️ Issues Found', '✅ No Issues') to improve speed of comprehension and accessibility.
