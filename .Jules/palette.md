## 2025-05-14 - Delayed Gratification and Progress Visualization
**Learning:** Initial animations (like balloons on page load) can be disruptive and lose their impact if shown too frequently. Coupling "moments of delight" with task completion creates a much stronger positive reinforcement loop. Visualizing progress (even in simple annotation tasks) reduces cognitive load and gives users a sense of accomplishment.
**Action:** Use `st.progress` to track task completion and save celebratory animations (`st.balloons`, `st.snow`) for terminal success states rather than initial load.
