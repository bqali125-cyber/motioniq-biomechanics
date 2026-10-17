# Security and Privacy Policy for MotionIQ

## 1. Local-First Processing
- **Zero Cloud Transmission:** Video frames, biometric estimations, and landmark coordinates are processed locally on the host device.
- **No Third-Party Analytics:** MotionIQ does not embed telemetry, tracking scripts, or external network hooks during video analysis.

## 2. File Handling & Storage Safety
- **Non-Destructive:** MotionIQ opens video files in read-only mode (`cv2.VideoCapture`). Input files are never overwritten, renamed, or modified.
- **Isolated Session Storage:** All generated telemetry, videos, and JSON reports are saved into isolated subdirectories under `outputs/session_<id>/`.
- **Input Sanitization:** Video paths are checked for traversal and validated against a whitelist of standard media extensions (`.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`). File size limits (default 500 MB) protect against out-of-memory denial of service.

## 3. Reporting a Vulnerability
If you discover a security or privacy vulnerability, please do not disclose it publicly. File a secure report or review the local configuration parameters in `motioniq/config.py`.
