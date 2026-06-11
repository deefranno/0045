## 2025-05-14 - [Gated Celebratory Effects]
**Learning:** For task-oriented apps (like annotation tools), gate celebratory effects like 'st.balloons()' behind a completion milestone (100% progress) instead of firing on initial load to provide a clear reward signal and avoid distraction.
**Action:** Move initialization-time balloons to conditional blocks triggered by success states or completion thresholds.

## 2025-05-14 - [Implicit String Concatenation in Data]
**Learning:** When defining multi-line strings in Python lists without commas, beware of implicit concatenation which can remove intended spaces between segments (e.g., 'is' 'and' becomes 'isand').
**Action:** Always include explicit spaces at the end of strings or use proper list comma separation to ensure data integrity.
