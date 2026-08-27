## 2023-10-27 - Frontend API Request Debouncing
**Learning:** The static HTML frontend in VisionLangWeb handles large image uploads via native fetch but previously lacked debouncing or button disabling during requests, creating a bottleneck where users could spam upload massive payloads, unnecessarily consuming network bandwidth and backend processing.
**Action:** Always verify that interactive submission buttons in raw HTML/JS frontends disable themselves (e.g., `button.disabled = true`) and re-enable in a `finally` block to prevent duplicate expensive network requests.
