## 2025-05-15 - [Gating Celebratory Effects]
**Learning:** For task-oriented apps like annotation tools, gating celebratory effects (e.g., balloons) behind a completion milestone (100% progress) provides a clear reward signal and avoids distracting the user during their workflow. Using session state to ensure the effect only fires once per session prevents user annoyance during subsequent interactions.
**Action:** Always check for '100% completion' logic before adding celebratory UI elements; use session state flags to gate these interactions.
