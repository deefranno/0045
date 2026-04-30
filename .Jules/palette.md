## 2025-05-15 - Enhancing Progress Tracking and Completion Feedback
**Learning:** In data-heavy Streamlit apps, celebratory animations like `st.balloons()` should be used sparingly and tied to meaningful milestones (e.g., 100% completion) rather than triggering on every script rerun. Using `st.session_state` to gate these animations prevents repetitive UI fatigue.
**Action:** Use `st.session_state` to track one-time UI events and combine `st.progress` with semantic metric labels to provide continuous feedback during long-running tasks.
