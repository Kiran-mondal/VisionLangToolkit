## 2023-10-27 - Frontend API Request Debouncing
**Learning:** The static HTML frontend in VisionLangWeb handles large image uploads via native fetch but previously lacked debouncing or button disabling during requests, creating a bottleneck where users could spam upload massive payloads, unnecessarily consuming network bandwidth and backend processing.
**Action:** Always verify that interactive submission buttons in raw HTML/JS frontends disable themselves (e.g., `button.disabled = true`) and re-enable in a `finally` block to prevent duplicate expensive network requests.

## 2024-05-30 - PIL Image Processing Optimization
**Learning:** In the Python backend (`main.py`), resizing large images (like 4K) for color extraction using `convert()` then `resize()` was taking ~0.15s. Using `thumbnail()` before `convert()` takes only ~0.01s because `thumbnail()` modifies the image in-place, preserves aspect ratio, and utilizes faster internal scaling logic specifically optimized for formats like JPEG where it uses drafting to avoid reading the entire image into memory.
**Action:** Always prefer `thumbnail()` over `resize()` when shrinking images for analysis where precise pixel manipulation is not required, and perform it *before* format conversions (like `convert('RGB')`) to minimize the amount of data being converted.
