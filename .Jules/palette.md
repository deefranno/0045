## 2026-06-10 - Gated Celebratory Feedback
**Learning:** For task-oriented applications like data annotation tools, firing celebratory effects (e.g., balloons) on initial load or every refresh can be distracting and loses its impact. Gating these effects behind a 100% completion milestone provides a clear reward signal and a sense of achievement.
**Action:** Always wrap celebratory components in conditional logic that checks for task completion (e.g., `if progress == 1.0:`).
