## 2025-08-25 - [Path Traversal in File Upload]
**Vulnerability:** The Python backend (`main.py`) directly used the user-provided `file.filename` in `os.path.join` to construct the save path for temporary image files, allowing an attacker to write arbitrary files to the server using directory traversal sequences (e.g., `../../../tmp/pwned`).
**Learning:** Even temporary or intermediate files need sanitized names because Python's `os.path.join` will resolve absolute paths or traverse directories if provided in the rightmost arguments.
**Prevention:** Always sanitize user-provided filenames using a robust library function like Werkzeug's `secure_filename()` before using them in file system operations.
