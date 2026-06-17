## 2025-05-15 - Preventing Balloon Fatigue in Streamlit
**Learning:** In Streamlit, every user interaction triggers a full script rerun. Visual effects like `st.balloons()` or `st.snow()` can become repetitive and annoying if they fire on every interaction.
**Action:** Always wrap one-time visual delights in a `st.session_state` check to ensure they only execute once per user session.
