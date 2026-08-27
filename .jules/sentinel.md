## 2025-08-25 - [Path Traversal in File Upload]
**Vulnerability:** The Python backend (`main.py`) directly used the user-provided `file.filename` in `os.path.join` to construct the save path for temporary image files, allowing an attacker to write arbitrary files to the server using directory traversal sequences (e.g., `../../../tmp/pwned`).
**Learning:** Even temporary or intermediate files need sanitized names because Python's `os.path.join` will resolve absolute paths or traverse directories if provided in the rightmost arguments.
**Prevention:** Always sanitize user-provided filenames using a robust library function like Werkzeug's `secure_filename()` before using them in file system operations.
## 2026-08-27 - [Information Leakage via Error Handling]
**Vulnerability:** The Python backend (`main.py`) caught exceptions globally in the `/analyze` endpoint and returned the raw exception string (`str(e)`) directly to the client in the JSON error response.
**Learning:** Returning raw error details or stack traces to the client can expose sensitive internal system details, library versions, or file paths, which attackers can use to gather intelligence for further attacks.
**Prevention:** Always catch exceptions securely by logging the detailed error (including stack traces if needed) server-side and returning a generic, safe error message to the client (e.g., 'An internal server error occurred').
