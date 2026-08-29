## 2025-08-25 - [Path Traversal in File Upload]
**Vulnerability:** The Python backend (`main.py`) directly used the user-provided `file.filename` in `os.path.join` to construct the save path for temporary image files, allowing an attacker to write arbitrary files to the server using directory traversal sequences (e.g., `../../../tmp/pwned`).
**Learning:** Even temporary or intermediate files need sanitized names because Python's `os.path.join` will resolve absolute paths or traverse directories if provided in the rightmost arguments.
**Prevention:** Always sanitize user-provided filenames using a robust library function like Werkzeug's `secure_filename()` before using them in file system operations.
## 2026-08-27 - [Information Leakage via Error Handling]
**Vulnerability:** The Python backend (`main.py`) caught exceptions globally in the `/analyze` endpoint and returned the raw exception string (`str(e)`) directly to the client in the JSON error response.
**Learning:** Returning raw error details or stack traces to the client can expose sensitive internal system details, library versions, or file paths, which attackers can use to gather intelligence for further attacks.
**Prevention:** Always catch exceptions securely by logging the detailed error (including stack traces if needed) server-side and returning a generic, safe error message to the client (e.g., 'An internal server error occurred').
## 2026-08-26 - Information Leakage & Missing Input Validation in Flask API
**Vulnerability:** The `/analyze` endpoint lacked input validation (allowing non-image files to be uploaded and processed) and suffered from information leakage (the global exception handler directly returned the raw `str(e)` of any exception to the client).
**Learning:** Returning direct exception strings to the client can expose internal stack traces, dependency details, or configuration information which attackers could exploit. Processing files without checking their `content_type` can also lead to Denial of Service or code execution via malicious payloads.
**Prevention:** Always validate file input (e.g. `file.content_type.startswith('image/')`) before processing. Implement generic error messages (e.g., "An internal processing error occurred") for client-facing 5xx responses, while securely logging the actual error details server-side.
## 2026-08-28 - [Cross-Site Scripting (XSS) via Third-Party API]
**Vulnerability:** The frontend (`VisionLangWeb/index.html`) fetched color names from a third-party API (`thecolorapi.com`) and injected them directly into the DOM using `innerHTML` without sanitization. This created an XSS risk if the external API were compromised or returned malicious script tags.
**Learning:** Never trust data from external sources or third-party APIs. Even seemingly benign data like "color names" must be sanitized before rendering as HTML to prevent injection attacks.
**Prevention:** Always use safe DOM manipulation methods (like `textContent`) or thoroughly sanitize untrusted data using an HTML escape function before using `innerHTML`.
## 2026-08-29 - [Missing Security Headers in Flask API]
**Vulnerability:** The Flask API (`main.py`) was not setting standard HTTP security headers (e.g., `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`).
**Learning:** Missing security headers expose the application to MIME-sniffing, framing attacks (clickjacking), and potential downgrades of secure connections.
**Prevention:** Always implement a response hook (like `@app.after_request` in Flask) or use a library (like Flask-Talisman) to inject strong security headers globally on all API responses.
