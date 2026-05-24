## 2025-05-22 - [Celebratory UX Gating]
**Learning:** For task-oriented apps (like annotation tools), gate celebratory effects like 'st.balloons()' behind a completion milestone (100% progress) instead of firing on initial load to provide a clear reward signal and avoid distraction.
**Action:** Use 'st.session_state' to track completion and ensure celebratory animations trigger exactly once upon reaching milestones.
