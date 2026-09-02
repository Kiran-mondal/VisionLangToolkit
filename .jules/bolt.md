## 2023-10-27 - Frontend API Request Debouncing
**Learning:** The static HTML frontend in VisionLangWeb handles large image uploads via native fetch but previously lacked debouncing or button disabling during requests, creating a bottleneck where users could spam upload massive payloads, unnecessarily consuming network bandwidth and backend processing.
**Action:** Always verify that interactive submission buttons in raw HTML/JS frontends disable themselves (e.g., `button.disabled = true`) and re-enable in a `finally` block to prevent duplicate expensive network requests.

## 2024-05-30 - PIL Image Processing Optimization
**Learning:** In the Python backend (`main.py`), resizing large images (like 4K) for color extraction using `convert()` then `resize()` was taking ~0.15s. Using `thumbnail()` before `convert()` takes only ~0.01s because `thumbnail()` modifies the image in-place, preserves aspect ratio, and utilizes faster internal scaling logic specifically optimized for formats like JPEG where it uses drafting to avoid reading the entire image into memory.
**Action:** Always prefer `thumbnail()` over `resize()` when shrinking images for analysis where precise pixel manipulation is not required, and perform it *before* format conversions (like `convert('RGB')`) to minimize the amount of data being converted.

## 2024-05-24 - [Pillow Image.copy() Defeats Thumbnail Lazy-Loading]
**Learning:** Using `Image.copy()` before `thumbnail()` in Pillow forces a full image decode to memory, completely defeating the built-in lazy-loading and fast scaling optimizations of `thumbnail()`. This can make thumbnail generation up to 10x slower on large images.
**Action:** Instead of creating a copy of the image to preserve its original state (e.g. `mode`), extract and cache the needed properties (like `original_mode = img.mode`) first, then apply `thumbnail()` directly to the original `Image` object.

## 2024-05-31 - Client-Side Caching for External APIs
**Learning:** In the static HTML frontend (`VisionLangWeb/index.html`), the application fetches color names for image palettes using an external API (`thecolorapi.com`). This resulted in redundant network requests when multiple images shared similar dominant colors or the same image was uploaded again, blocking rendering and slowing down the UI.
**Action:** Implement a client-side in-memory cache (like a JavaScript `Map`) for external API responses that represent static mappings (e.g., Hex codes to Color names). Check the cache before initiating `fetch` requests to reduce latency and save network bandwidth on subsequent operations.

## 2024-05-31 - Extreme Downscaling and Resampling for Color Quantization
**Learning:** For extracting dominant colors using `img.quantize()`, generating a high-quality or reasonably large thumbnail (like 150x150 with default BICUBIC or LANCZOS resampling) is unnecessary and wastes CPU cycles. Shrinking the thumbnail further to 50x50 and switching to `Image.Resampling.NEAREST` drops thumbnail generation time by ~50% (from ~10ms down to ~5ms for 4K images) while still providing enough pixels to extract the top 5 dominant colors reliably. Also, `quantize()` can return a palette smaller than requested if the image lacks color variety (e.g., solid color images), which can cause `IndexError` when naively looping over a fixed range.
**Action:** When resizing images purely for global color or mood extraction, aggressively downscale (e.g., 50x50) and use `resample=Image.Resampling.NEAREST`. Always handle edge cases where `quantize()` returns fewer colors than expected by checking the palette length.

## 2024-05-31 - Caching Promises for Parallel External API Requests
**Learning:** In the static HTML frontend (`VisionLangWeb/index.html`), caching the resolved color name in an external API request mapping (Hex to Name) doesn't prevent redundant requests when processing duplicate hex codes concurrently (e.g., when the backend pads missing colors with multiple `#FFFFFF` entries). The `map(async)` creates multiple parallel fetches before any of them resolve and populate the cache, rendering the cache ineffective for intra-upload duplicates.
**Action:** When implementing client-side caching for data loaded concurrently (such as mapping over an array of items), store the *Promise* of the fetch operation in the cache immediately, rather than waiting for the resolved value. Subsequent parallel iterations will then `await` the already-in-flight Promise instead of initiating duplicate network requests.
