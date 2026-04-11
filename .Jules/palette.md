## 2025-05-14 - Conditional Celebration Feedback
**Learning:** Using `st.balloons()` on every app load can be intrusive and loses its celebratory meaning. Celebratory animations should be reserved for terminal success states (e.g., finishing a task) and gated with `st.session_state` to prevent repetitive firing on every script rerun.
**Action:** Always use `st.session_state` to track task completion and ensure success animations only fire once per milestone.
