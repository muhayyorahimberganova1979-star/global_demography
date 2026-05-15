#!/usr/bin/env python3
"""
Global Demografiya Tahlili - Ishga tushiruvchi
===============================================
Backend va frontendni bir vaqtda ishga tushiradi
"""

import subprocess
import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')


def main():
    print("=" * 60)
    print("  🌍 Global Demografiya Tahlili Tizimi")
    print("=" * 60)
    print(flush=True)

    # Backend
    backend = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=BACKEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(2)

    # Frontend
    frontend = subprocess.Popen(
        [sys.executable, '-m', 'streamlit', 'run', 'app.py',
         '--server.port', '8501',
         '--server.headless', 'true',
         '--browser.gatherUsageStats', 'false'],
        cwd=FRONTEND_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    print("=" * 60)
    print("  🌐 Sayt manzili: http://localhost:8501")
    print("=" * 60)
    print()
    print("  To'xtatish uchun: Ctrl+C")
    print("-" * 60, flush=True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹ To'xtatilmoqda...")
        backend.terminate()
        frontend.terminate()
        print("✅ Tizim to'xtatildi.")


if __name__ == '__main__':
    main()
