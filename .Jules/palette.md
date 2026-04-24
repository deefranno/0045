## 2026-04-24 - Enhance Completion Experience and Visual Feedback
**Learning:** In data annotation tools, immediate but non-intrusive feedback (like progress bars) improves user focus, while reserving celebratory animations (like balloons) for terminal states prevents cognitive overload. Gating celebrations with session state ensures they remain a delight rather than a distraction on every rerun.
**Action:** Use `st.progress` for active tracking and `st.session_state` to gate terminal success animations.
