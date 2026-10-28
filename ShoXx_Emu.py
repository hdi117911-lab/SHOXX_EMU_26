#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShoXx_Emu - Main Portable Launcher Entrypoint
Starts the Crazy Neon Tkinter GUI in PC Fullscreen with Graffiti Splash Screen,
One-Click Auto-Setup, Android 17 (API 37) Studio Emulator, and Switchable Root Access.
"""

import os
import sys

# Ensure src/ is on sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from shoxx_gui import ShoXxApp


def main():
    auto_boot = "--auto-boot" in sys.argv
    app = ShoXxApp(auto_boot=auto_boot)
    app.mainloop()


if __name__ == "__main__":
    main()
