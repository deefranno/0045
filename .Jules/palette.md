## 2026-05-19 - [Streamlit Completion UX]
**Learning:** Moving celebratory animations (like st.balloons) from initial load to a conditional completion state (e.g., 100% progress) provides a more meaningful reward for user interaction. Using st.session_state to gate these animations ensures they only fire once, preventing repetitive and distracting triggers on every rerun.
**Action:** Always consider gating "delight" animations behind specific user-achieved milestones rather than generic page events.
