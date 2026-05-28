## 2025-05-28 - Gated Celebration Milestones
**Learning:** In task-oriented applications like annotation tools, triggering celebratory effects (e.g., `st.balloons()`) on initial load can be distracting. Gating them behind a 100% completion milestone provides a much stronger positive reinforcement and a clear signal of task finished.
**Action:** Always use session state to ensure milestone celebrations fire exactly once when the threshold is reached, and pair them with persistent progress indicators.
