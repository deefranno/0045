## 2026-06-04 - [Reward Signaling with Gated Celebrations]
**Learning:** For task-oriented apps (like annotation tools), gate celebratory effects like `st.balloons()` behind a completion milestone (100% progress) instead of firing on initial load. This provides a clear reward signal and avoids distracting the user before they've started the task.
**Action:** Always check for a logical completion state before triggering major animations or celebratory UI elements.
