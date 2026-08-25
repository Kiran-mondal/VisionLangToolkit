## 2026-08-25 - Avoid Disk I/O for Uploaded Files
**Learning:** Writing uploaded images to a temporary directory in Flask just so PIL can open them via path induces a significant performance penalty (roughly ~78% slower in benchmarks) and consumes unnecessary server storage. `Image.open()` in PIL fully supports reading directly from `request.files['image'].stream`.
**Action:** Always prefer passing in-memory file streams directly to libraries like PIL rather than creating temporary files on disk, especially in high-throughput endpoints.
