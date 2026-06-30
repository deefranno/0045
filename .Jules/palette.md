## 2024-06-30 - Improving Streamlit Interactive Clarity
**Learning:** In Streamlit, boolean data columns in filters are often displayed as raw True/False values, which can be confusing for non-technical users. Additionally, "one-time" visual effects like st.balloons() trigger on every rerun unless wrapped in a session state check.
**Action:** Always use `format_func` in st.selectbox to map raw data values to human-readable labels, and wrap session-start effects in st.session_state checks.
