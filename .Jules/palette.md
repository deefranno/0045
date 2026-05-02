## 2025-05-15 - [Streamlit Progressive Disclosure & Celebration]
**Learning:** Using `st.session_state` to gate celebratory animations (like `st.balloons`) prevents them from becoming a nuisance on every script rerun while still providing a delightful "A-ha!" moment upon task completion. Pairing this with a persistent `st.success` message ensures the positive state remains visible after the animation ends.
**Action:** Always gate terminal success animations with session state and provide a companion persistent status message.
