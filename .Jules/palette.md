## 2025-06-02 - Gating celebrations for better reward signals
**Learning:** For task-oriented apps (like annotation tools), gate celebratory effects like 'st.balloons()' behind a completion milestone (100% progress) instead of firing on initial load to provide a clear reward signal and avoid distraction.
**Action:** Use st.session_state to track milestone triggers and only fire st.balloons() when a progress threshold is met for the first time in a session.
