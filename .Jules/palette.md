## 2025-06-13 - Milestone-Gated Celebration
**Learning:** For task-oriented applications like data annotation tools, firing celebratory effects (e.g., `st.balloons()`) on initial page load can be distracting and loses its impact. Gating these effects behind a 100% completion milestone provides a much stronger reward signal and encourages task completion.
**Action:** Always use `st.session_state` to track and trigger celebratory milestones only once upon reaching a completion goal, rather than on every page refresh or initial load.
