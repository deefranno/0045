## 2025-05-15 - Improving Feedback Loops in Data Annotation
**Learning:** Initial application load animations like `st.balloons()` create unnecessary cognitive load and distract from the primary task. Celebratory feedback should be reserved for terminal success states to maintain its reward value.
**Action:** Relocate celebratory animations to the completion of the annotation process and gate them with session state to prevent repetitive firing.
