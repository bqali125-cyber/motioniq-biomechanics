"""
MotionIQ — Single-File Launcher / فایل اجرای آسان با یک کلیک.
Automatically configures the environment, launches the web interface, and opens your browser.
"""

from __future__ import annotations
import os
import sys
import subprocess
import webbrowser
import threading
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe"


def main():
    # 1. Ensure execution within the configured Python 3.11 virtual environment
    if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
        print(f"[MotionIQ Launcher] Routing execution to virtual environment: {VENV_PYTHON}")
        try:
            subprocess.run([str(VENV_PYTHON), str(__file__)] + sys.argv[1:], check=True)
        except KeyboardInterrupt:
            print("\n[MotionIQ] Server terminated by user.")
        sys.exit(0)

    # Add root directory to sys.path so motioniq package is always importable
    if str(ROOT_DIR) not in sys.path:
        sys.path.insert(0, str(ROOT_DIR))

    # 2. Verify model files exist in models/, if not download standard models
    from scripts.download_models import download_model
    full_model = ROOT_DIR / "models" / "pose_landmarker_full.task"
    if not full_model.exists():
        print("[MotionIQ Launcher] Initializing model cache...")
        download_model("full")

    # 3. Verify sample video exists
    sample_video = ROOT_DIR / "examples" / "sample_squat.mp4"
    if not sample_video.exists():
        print("[MotionIQ Launcher] Generating sample test video...")
        from examples.generate_sample_video import generate_sample_squat_video
        generate_sample_squat_video(sample_video)

    # 4. Free port 7860 if occupied by a previous zombie instance
    if os.name == "nt":
        try:
            cmd = 'powershell -Command "Get-NetTCPConnection -LocalPort 7860 -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.5)
        except Exception:
            pass

    # 5. Launch Gradio Web Application
    from app.main import build_app

    PORT = 7860
    HOST = "127.0.0.1"
    URL = f"http://{HOST}:{PORT}"

    print("=" * 65)
    print("🏃‍♂️ MotionIQ — سامانه ارزیابی و تحلیل هوشمند حرکت انسان")
    print(f"🌐 آدرس وب‌سرور: {URL}")
    print("🚀 مرورگر به صورت خودکار باز می‌شود...")
    print("=" * 65)

    def open_browser():
        time.sleep(1.2)
        webbrowser.open(URL)

    threading.Thread(target=open_browser, daemon=True).start()

    app = build_app()
    app.launch(
        server_name=HOST,
        server_port=PORT,
        inbrowser=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
