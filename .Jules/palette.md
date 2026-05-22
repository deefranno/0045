# Palette's UX Journal

## 2025-05-15 - Reward-based Feedback Loop
**Learning:** In annotation tasks, immediate celebratory animations like `st.balloons()` on page load can be confusing and distracting. Gating them behind a completion milestone (e.g., 100% progress) provides a clear "job well done" signal and improves the user's sense of accomplishment.
**Action:** Use session state to track milestone completion and trigger animations only once when the goal is reached.
