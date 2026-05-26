# Palette's Journal - UX & Accessibility

## 2024-05-26 - Task-driven Celebrations
**Learning:** For task-oriented apps (like annotation tools), gating celebratory effects like `st.balloons()` behind a completion milestone (100% progress) instead of firing on initial load provides a clear reward signal and avoids distraction. Using `st.session_state` ensures the animation only plays once upon reaching the goal.
**Action:** Always gate heavy animations or celebrations behind specific user achievements or state transitions.

## 2024-05-26 - Implicit String Spacing
**Learning:** In Python, implicitly concatenated multiline strings (e.g., `"a" "b"`) do not include a space between them. This can lead to "squashed" text in UI components if not handled carefully.
**Action:** Use explicit spaces at the end of string segments or use triple-quoted strings for multiline text to ensure readability.
