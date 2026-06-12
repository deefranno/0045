## 2026-06-12 - Gating Celebratory Effects and Visual Progress tracking
**Learning:** For task-oriented apps like annotation tools, firing celebratory effects like 'st.balloons()' on initial load is distracting and lacks a reward signal. UX is improved by gating these behind a completion milestone (100% progress) and providing an immediate visual progress indicator like 'st.progress' to keep the user informed and motivated.
**Action:** Always gate 'st.balloons()' behind a completion check and pair 'st.metric' progress with 'st.progress' for better visual feedback.
