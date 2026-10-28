# ⚡ ShoXx_Emu // Portable Pixel 9 Pro XL Emulator (Android 15 / 16 / 17 + Multi-Root)

**ShoXx_Emu** ist ein vollständig autonomer, portabler Android-Emulator auf Basis der offiziellen **Android Studio QEMU/Gfxstream Engine**, gesteuert über eine **Crazy Neon Cyberpunk Tkinter GUI** mit:
- **Android 15 (API 35)**, **Android 16 (API 36)** und **Android 17 (API 37)** zur direkten Auswahl (alle 3 System-Images & Plattformen komplett im Ordner gebündelt!).
- **Aktuelles Google Pixel Flagship-Profil (`Google Pixel 9 Pro XL`, `Pixel 9 Pro`, `Pixel 9 Pro Fold`)**, das randlos im **PC-Vollbildmodus** auf dem Monitor startet.
- **Zuschaltbarem Root-Zugriff per Schalter (`ROOT SWITCH [ON/OFF]`)** mit **3 wählbaren Root-Methoden**:
  1. **Magisk (`v31.1`)** – Zygisk + native `x86_64` Binaries (`magisk`, `magiskinit`, `magiskpolicy`, `busybox`) + Magisk Manager APK.
  2. **KernelSU (`v3.3.1`)** – Kernel-basierter `x86_64` `ksud` & `libadbroot.so` Daemon + KernelSU Manager APK.
  3. **Alternative: APatch (`11282`) + Native SuperSU Bridge** – Native `adbd uid=0` Root-Bridge, `/system` R/W-Remount, `SELinux Permissive`, `BusyBox x86_64` + APatch Manager APK.
- **2-Stufen Graffiti & System-Diagnose Splash-Screen** sowie **animierter Plugin-/Tool-Matrix** und **Echtzeit-Hardware-Analyse (CPU, RAM, GPU, Hypervisor)** inkl. **Vorschlag optimaler Settings**.

---

## 🚀 Starten (One-Click)

- **Standard Start (Vollbild-GUI + Graffiti & Diagnose Splash-Screen + OS-/Root-Auswahl)**:
  Doppelklick auf [`One_Click_Start_ShoXx_Emu.bat`](file:///d:/SHOXX_EMU_26/One_Click_Start_ShoXx_Emu.bat) oder:
  ```powershell
  .\python_portable\python.exe .\ShoXx_Emu.py
  ```
- **Sofortiger Auto-Boot in PC-Vollbild + Root**:
  Doppelklick auf [`Auto_Boot_Android17_Fullscreen.bat`](file:///d:/SHOXX_EMU_26/Auto_Boot_Android17_Fullscreen.bat) oder:
  ```powershell
  .\python_portable\python.exe .\ShoXx_Emu.py --auto-boot
  ```
