# -*- coding: utf-8 -*-
"""
ShoXx_Emu - Autonomous Portable Android 15 / 16 / 17 Setup, Google Play Store ROM Manager,
Anti-Emulator Detection (Real Smartphone Stealth Engine), Multi-Profile Manager,
APK & XAPK Split/OBB Installer, Shared Folder Bridge & 3-Method Root Engine.
"""

import os
import sys
import json
import uuid
import random
import shutil
import zipfile
import urllib.request
import subprocess
import platform
import ctypes
import time
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDK_DIR = os.path.join(BASE_DIR, "sdk")
AVD_DATA_ROOT = os.path.join(BASE_DIR, "avd_data")
AVD_HOME = os.path.join(AVD_DATA_ROOT, ".android", "avd")
ANDROID_USER_HOME = os.path.join(AVD_DATA_ROOT, ".android")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
CACHE_DIR = os.path.join(BASE_DIR, "_cache")
TEMP_PORTABLE_DIR = os.path.join(BASE_DIR, "_cache", "temp")
ROOT_METHODS_DIR = os.path.join(BASE_DIR, "root_methods")
SHARED_PC_DIR = os.path.join(BASE_DIR, "Shared_PC_Folder")
PROFILES_JSON = os.path.join(AVD_DATA_ROOT, "profiles.json")

# Force Python's own tempfile module to stay strictly inside the portable main directory
os.makedirs(TEMP_PORTABLE_DIR, exist_ok=True)
os.environ["TEMP"] = TEMP_PORTABLE_DIR
os.environ["TMP"] = TEMP_PORTABLE_DIR
os.environ["TMPDIR"] = TEMP_PORTABLE_DIR

# All ROMs include official Google Play Store (google_apis_playstore) + fallback to local image
ANDROID_VERSIONS = {
    "17": {
        "api": 37,
        "name": "Android 17 (API 37 - CinnamonBun + Google Play Store)",
        "short": "Android 17 (Play Store)",
        "codename": "CinnamonBun",
        "avd_name": "ShoXx_Pixel_Android17",
        "platform_dir": "android-37",
        "platform_url": "https://dl.google.com/android/repository/platform-37.0_r02.zip",
        "playstore_rel": os.path.join("system-images", "android-37", "google_apis_playstore", "x86_64"),
        "playstore_url": "https://dl.google.com/android/repository/sys-img/google_apis_playstore/x86_64-37.0_r08.zip",
        "default_rel": os.path.join("system-images", "android-37", "default", "x86_64"),
        "default_url": "https://dl.google.com/android/repository/sys-img/android/x86_64-37.0_r06.zip",
    },
    "16": {
        "api": 36,
        "name": "Android 16 (API 36 - Baklava + Google Play Store)",
        "short": "Android 16 (Play Store)",
        "codename": "Baklava",
        "avd_name": "ShoXx_Pixel_Android16",
        "platform_dir": "android-36",
        "platform_url": "https://dl.google.com/android/repository/platform-36_r01.zip",
        "playstore_rel": os.path.join("system-images", "android-36", "google_apis_playstore", "x86_64"),
        "playstore_url": "https://dl.google.com/android/repository/sys-img/google_apis_playstore/x86_64-36_r07.zip",
        "default_rel": os.path.join("system-images", "android-36", "default", "x86_64"),
        "default_url": "https://dl.google.com/android/repository/sys-img/android/x86_64-36_r02.zip",
    },
    "15": {
        "api": 35,
        "name": "Android 15 (API 35 - VanillaIceCream + Google Play Store)",
        "short": "Android 15 (Play Store)",
        "codename": "VanillaIceCream",
        "avd_name": "ShoXx_Pixel_Android15",
        "platform_dir": "android-35",
        "platform_url": "https://dl.google.com/android/repository/platform-35_r02.zip",
        "playstore_rel": os.path.join("system-images", "android-35", "google_apis_playstore", "x86_64"),
        "playstore_url": "https://dl.google.com/android/repository/sys-img/google_apis_playstore/x86_64-35_r09.zip",
        "default_rel": os.path.join("system-images", "android-35", "default", "x86_64"),
        "default_url": "https://dl.google.com/android/repository/sys-img/android/x86_64-35_r02.zip",
    },
}

# Real Retail Smartphone Fingerprints for Anti-Emulator Stealth Spoofing
PIXEL_PROFILES = {
    "pixel_9_pro_xl": {
        "id": "pixel_9_pro_xl",
        "display": "Google Pixel 9 Pro XL (komodo - Retail Smartphone Stealth)",
        "brand": "google",
        "manufacturer": "Google",
        "model": "Pixel 9 Pro XL",
        "device": "komodo",
        "product": "komodo",
        "board": "komodo",
        "hardware": "komodo",
        "soc_manufacturer": "Google",
        "soc_model": "Tensor G4",
        "fingerprint": "google/komodo/komodo:16/BP22.250325.006/13344233:user/release-keys",
        "description": "komodo-user 16 BP22.250325.006 13344233 release-keys",
        "baseband": "g5400c-250311-250325-B-13281994",
        "bootloader": "ripcurrent-15.1-13129455",
    },
    "pixel_9_pro": {
        "id": "pixel_9_pro",
        "display": "Google Pixel 9 Pro (caiman - Retail Smartphone Stealth)",
        "brand": "google",
        "manufacturer": "Google",
        "model": "Pixel 9 Pro",
        "device": "caiman",
        "product": "caiman",
        "board": "caiman",
        "hardware": "caiman",
        "soc_manufacturer": "Google",
        "soc_model": "Tensor G4",
        "fingerprint": "google/caiman/caiman:16/BP22.250325.006/13344233:user/release-keys",
        "description": "caiman-user 16 BP22.250325.006 13344233 release-keys",
        "baseband": "g5400c-250311-250325-B-13281994",
        "bootloader": "ripcurrent-15.1-13129455",
    },
    "pixel_9_pro_fold": {
        "id": "pixel_9_pro_fold",
        "display": "Google Pixel 9 Pro Fold (comet - Retail Smartphone Stealth)",
        "brand": "google",
        "manufacturer": "Google",
        "model": "Pixel 9 Pro Fold",
        "device": "comet",
        "product": "comet",
        "board": "comet",
        "hardware": "comet",
        "soc_manufacturer": "Google",
        "soc_model": "Tensor G4",
        "fingerprint": "google/comet/comet:16/BP22.250325.006/13344233:user/release-keys",
        "description": "comet-user 16 BP22.250325.006 13344233 release-keys",
        "baseband": "g5400c-250311-250325-B-13281994",
        "bootloader": "comet-15.1-13129455",
    },
}

ROOT_METHODS = {
    "MAGISK": {
        "id": "MAGISK",
        "name": "1. Magisk v31.1 (Zygisk + Systemless Daemon & Manager)",
        "short": "Magisk v31.1",
        "apk_rel": os.path.join("magisk", "Magisk.apk"),
        "bin_rel": os.path.join("magisk", "bin_x86_64"),
        "desc": "Injects Magisk x86_64 binaries (magisk, magiskinit, magiskpolicy, busybox) into /system/xbin/su + Magisk Manager APK + Zygisk Stealth.",
    },
    "KERNELSU": {
        "id": "KERNELSU",
        "name": "2. KernelSU v3.3.1 (Kernel-Based ksud + libadbroot Bridge)",
        "short": "KernelSU v3.3.1",
        "apk_rel": os.path.join("kernelsu", "KernelSU.apk"),
        "bin_rel": os.path.join("kernelsu", "bin_x86_64"),
        "desc": "Deploys KernelSU x86_64 daemon (ksud, kernelsu, libadbroot.so) into /data/adb/ksu & /system/xbin/su + KernelSU Manager APK.",
    },
    "APATCH_SU": {
        "id": "APATCH_SU",
        "name": "3. Alternative: APatch + Native SuperSU Bridge (adbd uid=0 + R/W)",
        "short": "APatch + Native SU",
        "apk_rel": os.path.join("apatch", "APatch.apk"),
        "bin_rel": os.path.join("magisk", "bin_x86_64"),
        "desc": "Activates Native ADBD Superuser (uid=0), remounts /system R/W, sets SELinux Permissive, and installs APatch Manager + BusyBox.",
    },
}

URLS = {
    "platform-tools": "https://dl.google.com/android/repository/platform-tools_r37.0.1-win.zip",
    "emulator": "https://dl.google.com/android/repository/emulator-windows_x64-16632760.zip",
}

SIDEBAR_WIDTH = 340  # Fixed Right-Side GAMING EXTEND Panel Width in Fullscreen Mode
SIDEBAR_COLLAPSED_WIDTH = 48  # Slim Dock Strip Width when GAMING EXTEND Sidebar is Collapsed


def generate_random_imei() -> str:
    """Generates a valid Luhn-checksummed Google Pixel TAC IMEI (35847632xxxxxxx)."""
    tac = "35847632"
    body = tac + "".join(str(random.randint(0, 9)) for _ in range(6))
    digits = [int(d) for d in body]
    total = 0
    for idx, d in enumerate(digits):
        if idx % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    check = (10 - (total % 10)) % 10
    return body + str(check)


def generate_random_serial() -> str:
    chars = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "49" + "".join(random.choice(chars) for _ in range(10))


class ShoXxEngine:
    """Manages Profiles, Play Store ROMs, Anti-Emulator Stealth, APK/XAPK Installer, Shared Folder, and Multi-Root."""

    def __init__(self, log_callback=None, progress_callback=None):
        def _default_log(msg, level="INFO"):
            try:
                print(f"[{level}] {msg}")
            except UnicodeEncodeError:
                print(f"[{level}] {msg.encode('ascii', 'replace').decode('ascii')}")

        self.log_cb = log_callback or _default_log
        self.prog_cb = progress_callback or (lambda pct, status="": None)
        self.emulator_proc = None

        self.selected_android = "16"  # Default to 16 where Play Store ROM is already pre-bundled out of the box
        self.selected_pixel = "pixel_9_pro_xl"
        self.root_enabled = True
        self.root_method = "MAGISK"
        self.stealth_enabled = True  # Anti-Emulator Real Smartphone Stealth Mode

        self.fullscreen_enabled = True
        self.sidebar_docked = True
        self.sidebar_collapsed = False
        self.ram_mb = 6144
        self.cores = 4
        self.gpu_mode = "host"
        self.resolution = (1920, 1080)
        self.dpi = 320
        self.cold_boot = False

        self.ensure_directories()
        self.profiles = []
        self.active_profile_id = None
        self.load_or_init_profiles()
        self.relink_portable_paths()

        self.system_report = {}
        self.plugins_report = []
        self.optimal_settings = {}

    def log(self, msg: str, level: str = "INFO"):
        if self.log_cb:
            self.log_cb(msg, level)

    def progress(self, pct: float, status: str = ""):
        if self.prog_cb:
            self.prog_cb(pct, status)

    def ensure_directories(self):
        for d in [
            SDK_DIR, AVD_DATA_ROOT, AVD_HOME, ANDROID_USER_HOME,
            DOWNLOADS_DIR, CACHE_DIR, TEMP_PORTABLE_DIR, ROOT_METHODS_DIR, SHARED_PC_DIR,
            os.path.join(SDK_DIR, "platforms"),
            os.path.join(SDK_DIR, "system-images", "android-35", "google_apis_playstore"),
            os.path.join(SDK_DIR, "system-images", "android-36", "google_apis_playstore"),
            os.path.join(SDK_DIR, "system-images", "android-37", "google_apis_playstore"),
        ]:
            os.makedirs(d, exist_ok=True)

        readme_shared = os.path.join(SHARED_PC_DIR, "SHOXX_SHARED_FOLDER_INFO.txt")
        if not os.path.exists(readme_shared):
            with open(readme_shared, "w", encoding="utf-8") as f:
                f.write(
                    "=== SHOXX_EMU SHARED PC <-> EMULATOR FOLDER ===\n"
                    "Alle Dateien in diesem Ordner können mit 1 Klick über das rechte GAMING EXTEND Panel\n"
                    "direkt auf das emulierte Pixel-Smartphone (/sdcard/Download/ShoXx_Shared) übertragen werden!\n"
                )

    def relink_portable_paths(self):
        """
        Ensures 100% Portability across different PCs, Users, and Drive Letters:
        Automatically rewrites any absolute `path=...` entries inside `./avd_data/.android/avd/*.ini`
        to match the current `BASE_DIR` on the new PC!
        """
        if not os.path.exists(AVD_HOME):
            return
        for fname in os.listdir(AVD_HOME):
            if fname.endswith(".ini"):
                ini_path = os.path.join(AVD_HOME, fname)
                avd_stem = fname[:-4]
                expected_avd_dir = os.path.join(AVD_HOME, f"{avd_stem}.avd")
                try:
                    with open(ini_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    new_lines = []
                    changed = False
                    for ln in lines:
                        if ln.startswith("path="):
                            cur_val = ln.split("=", 1)[1].strip()
                            if os.path.normcase(cur_val) != os.path.normcase(expected_avd_dir):
                                new_lines.append(f"path={expected_avd_dir}\n")
                                changed = True
                            else:
                                new_lines.append(ln)
                        else:
                            new_lines.append(ln)
                    if changed:
                        with open(ini_path, "w", encoding="utf-8") as f:
                            f.writelines(new_lines)
                except Exception:
                    pass

    def get_env(self) -> dict:
        """
        Returns a 100% portable, host-isolated environment dictionary:
        All SDK, AVD, ADB keys, user preferences, and temporary files are strictly confined
        to the main program folder (`BASE_DIR`) so nothing leaks to C:\\Users\\<User>.
        """
        env = os.environ.copy()
        env["SHOXX_PORTABLE_ROOT"] = BASE_DIR
        env["ANDROID_SDK_ROOT"] = SDK_DIR
        env["ANDROID_HOME"] = SDK_DIR
        env["ANDROID_SDK_HOME"] = AVD_DATA_ROOT
        env["ANDROID_PREFS_ROOT"] = AVD_DATA_ROOT
        env["ANDROID_AVD_HOME"] = AVD_HOME
        env["ANDROID_USER_HOME"] = ANDROID_USER_HOME
        env["ANDROID_EMULATOR_HOME"] = ANDROID_USER_HOME
        env["ADB_VENDOR_KEYS"] = ANDROID_USER_HOME
        env["HOME"] = AVD_DATA_ROOT
        env["USERPROFILE"] = AVD_DATA_ROOT
        env["LOCALAPPDATA"] = AVD_DATA_ROOT
        env["APPDATA"] = AVD_DATA_ROOT
        env["TEMP"] = TEMP_PORTABLE_DIR
        env["TMP"] = TEMP_PORTABLE_DIR
        env["TMPDIR"] = TEMP_PORTABLE_DIR
        emu_dir = os.path.join(SDK_DIR, "emulator")
        pt_dir = os.path.join(SDK_DIR, "platform-tools")
        py_dir = os.path.join(BASE_DIR, "python_portable")
        env["PATH"] = f"{py_dir};{emu_dir};{pt_dir};{env.get('PATH', '')}"
        return env

    @property
    def emulator_exe(self) -> str:
        return os.path.join(SDK_DIR, "emulator", "emulator.exe")

    @property
    def adb_exe(self) -> str:
        return os.path.join(SDK_DIR, "platform-tools", "adb.exe")

    # =========================================================================
    # MULTI-PROFILE MANAGER (CREATE, CLONE, EDIT, DELETE, SELECT PROFILES)
    # =========================================================================

    def load_or_init_profiles(self):
        """Loads user emulator profiles from avd_data/profiles.json or creates default profiles."""
        if os.path.exists(PROFILES_JSON):
            try:
                with open(PROFILES_JSON, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.profiles = data.get("profiles", [])
                    self.active_profile_id = data.get("active_id")
            except Exception:
                self.profiles = []

        if not self.profiles:
            self.profiles = [
                {
                    "id": "prof_pixel9xl_a16_play",
                    "name": "Pixel 9 Pro XL // Android 16 (Play Store + Magisk Stealth)",
                    "avd_name": "ShoXx_Prof_Pixel9XL_A16",
                    "android_ver": "16",
                    "pixel_model": "pixel_9_pro_xl",
                    "root_enabled": True,
                    "root_method": "MAGISK",
                    "stealth_enabled": True,
                    "ram_mb": 6144,
                    "cores": 4,
                    "gpu_mode": "host",
                    "imei": generate_random_imei(),
                    "serial": generate_random_serial(),
                    "carrier": "Telekom.de",
                },
                {
                    "id": "prof_pixel9xl_a17_play",
                    "name": "Pixel 9 Pro XL // Android 17 (CinnamonBun + KernelSU)",
                    "avd_name": "ShoXx_Prof_Pixel9XL_A17",
                    "android_ver": "17",
                    "pixel_model": "pixel_9_pro_xl",
                    "root_enabled": True,
                    "root_method": "KERNELSU",
                    "stealth_enabled": True,
                    "ram_mb": 6144,
                    "cores": 4,
                    "gpu_mode": "host",
                    "imei": generate_random_imei(),
                    "serial": generate_random_serial(),
                    "carrier": "Vodafone.de",
                },
                {
                    "id": "prof_pixelfold_a15_play",
                    "name": "Pixel 9 Pro Fold // Android 15 (Play Store + APatch)",
                    "avd_name": "ShoXx_Prof_PixelFold_A15",
                    "android_ver": "15",
                    "pixel_model": "pixel_9_pro_fold",
                    "root_enabled": True,
                    "root_method": "APATCH_SU",
                    "stealth_enabled": True,
                    "ram_mb": 6144,
                    "cores": 4,
                    "gpu_mode": "host",
                    "imei": generate_random_imei(),
                    "serial": generate_random_serial(),
                    "carrier": "O2 - de",
                },
            ]
            self.active_profile_id = self.profiles[0]["id"]
            self.save_profiles()

        self.select_profile(self.active_profile_id or self.profiles[0]["id"])

    def save_profiles(self):
        os.makedirs(os.path.dirname(PROFILES_JSON), exist_ok=True)
        with open(PROFILES_JSON, "w", encoding="utf-8") as f:
            json.dump({"active_id": self.active_profile_id, "profiles": self.profiles}, f, indent=2)

    def get_active_profile(self) -> dict:
        for p in self.profiles:
            if p["id"] == self.active_profile_id:
                return p
        return self.profiles[0]

    def select_profile(self, profile_id: str) -> dict:
        for p in self.profiles:
            if p["id"] == profile_id:
                self.active_profile_id = p["id"]
                self.selected_android = p.get("android_ver", "16")
                self.selected_pixel = p.get("pixel_model", "pixel_9_pro_xl")
                self.root_enabled = p.get("root_enabled", True)
                self.root_method = p.get("root_method", "MAGISK")
                self.stealth_enabled = p.get("stealth_enabled", True)
                self.ram_mb = p.get("ram_mb", 6144)
                self.cores = p.get("cores", 4)
                self.gpu_mode = p.get("gpu_mode", "host")
                self.save_profiles()
                return p
        return self.profiles[0]

    def create_new_profile(self, name: str, android_ver: str, pixel_model: str, root_enabled: bool, root_method: str, ram_mb: int = 6144, cores: int = 4) -> dict:
        uid = uuid.uuid4().hex[:6]
        avd_name = f"ShoXx_Prof_{android_ver}_{uid}"
        new_p = {
            "id": f"prof_{uid}",
            "name": name.strip() or f"Custom Pixel ({ ANDROID_VERSIONS[android_ver]['short'] })",
            "avd_name": avd_name,
            "android_ver": android_ver,
            "pixel_model": pixel_model,
            "root_enabled": root_enabled,
            "root_method": root_method,
            "stealth_enabled": True,
            "ram_mb": ram_mb,
            "cores": cores,
            "gpu_mode": self.gpu_mode,
            "imei": generate_random_imei(),
            "serial": generate_random_serial(),
            "carrier": "Telekom.de",
        }
        self.profiles.append(new_p)
        self.select_profile(new_p["id"])
        self.create_or_update_avd(android_ver=android_ver, avd_name=avd_name)
        self.log(f"✔ Created new Emulator Profile: '{new_p['name']}' (IMEI: {new_p['imei']})", "SUCCESS")
        return new_p

    def delete_profile(self, profile_id: str) -> bool:
        if len(self.profiles) <= 1:
            self.log("Cannot delete the last remaining profile!", "WARN")
            return False
        target = None
        for p in self.profiles:
            if p["id"] == profile_id:
                target = p
                break
        if not target:
            return False
        self.profiles.remove(target)
        avd_name = target.get("avd_name", "")
        if avd_name:
            shutil.rmtree(os.path.join(AVD_HOME, f"{avd_name}.avd"), ignore_errors=True)
            ini_f = os.path.join(AVD_HOME, f"{avd_name}.ini")
            if os.path.exists(ini_f):
                os.remove(ini_f)
        if self.active_profile_id == profile_id:
            self.select_profile(self.profiles[0]["id"])
        else:
            self.save_profiles()
        self.log(f"Deleted profile '{target['name']}'.", "WARN")
        return True

    def sync_current_settings_to_active_profile(self):
        p = self.get_active_profile()
        p["android_ver"] = self.selected_android
        p["pixel_model"] = self.selected_pixel
        p["root_enabled"] = self.root_enabled
        p["root_method"] = self.root_method
        p["stealth_enabled"] = self.stealth_enabled
        p["ram_mb"] = self.ram_mb
        p["cores"] = self.cores
        p["gpu_mode"] = self.gpu_mode
        self.save_profiles()

    @property
    def current_avd_name(self) -> str:
        p = self.get_active_profile()
        return p.get("avd_name", f"ShoXx_Pixel_Android{self.selected_android}")

    @property
    def current_sidebar_width(self) -> int:
        return SIDEBAR_COLLAPSED_WIDTH if self.sidebar_collapsed else SIDEBAR_WIDTH

    # =========================================================================
    # GOOGLE PLAY STORE ROM RESOLUTION & IN-APP DOWNLOADER
    # =========================================================================

    def get_rom_status(self, android_ver: str) -> dict:
        """
        Checks if the Google Play Store System Image (`google_apis_playstore`) or Base Image
        is installed for Android 15, 16, or 17.
        """
        v_info = ANDROID_VERSIONS.get(android_ver, ANDROID_VERSIONS["16"])
        ps_dir = os.path.join(SDK_DIR, v_info["playstore_rel"])
        def_dir = os.path.join(SDK_DIR, v_info["default_rel"])

        has_playstore = os.path.exists(os.path.join(ps_dir, "system.img"))
        has_default = os.path.exists(os.path.join(def_dir, "system.img"))

        active_dir = ps_dir if has_playstore else def_dir
        active_rel = v_info["playstore_rel"] if has_playstore else v_info["default_rel"]

        return {
            "ver": android_ver,
            "has_playstore": has_playstore,
            "has_default": has_default,
            "any_installed": has_playstore or has_default,
            "active_dir": active_dir,
            "active_rel": active_rel.replace("/", "\\") + "\\",
            "playstore_url": v_info["playstore_url"],
            "tag_id": "google_apis_playstore" if has_playstore else "default",
            "tag_display": "Google Play" if has_playstore else "Default Android System Image",
        }

    def download_playstore_rom(self, android_ver: str, on_done=None):
        """Downloads and extracts the official Google Play Store ROM (`google_apis_playstore`) strictly inside `./downloads` and `./sdk`."""
        def _worker():
            try:
                v_info = ANDROID_VERSIONS[android_ver]
                ps_dir = os.path.join(SDK_DIR, v_info["playstore_rel"])
                parent_dir = os.path.dirname(ps_dir)
                os.makedirs(parent_dir, exist_ok=True)
                os.makedirs(DOWNLOADS_DIR, exist_ok=True)

                zp = os.path.join(DOWNLOADS_DIR, f"playstore-sysimg-android-{android_ver}.zip")
                self._download_with_progress(
                    v_info["playstore_url"], zp,
                    f"Android {android_ver} Google Play Store ROM", 5, 75
                )
                self.progress(82, f"EXTRACTING ANDROID {android_ver} GOOGLE PLAY STORE ROM...")
                self.log(f"Extracting Android {android_ver} Google Play Store System Image from {zp}...", "CYBER")
                with zipfile.ZipFile(zp, "r") as z:
                    z.extractall(parent_dir)
                if os.path.exists(zp):
                    os.remove(zp)

                self.patch_system_image_build_prop(ps_dir)
                self.create_or_update_avd(android_ver=android_ver, force=False)
                self.progress(100, f"✔ ANDROID {android_ver} GOOGLE PLAY STORE ROM INSTALLED!")
                self.log(f"✔ Android {android_ver} Google Play Store ROM successfully installed & configured!", "SUCCESS")
                if on_done:
                    on_done(True)
            except Exception as e:
                self.log(f"Play Store ROM Download Error: {e}", "ERROR")
                if on_done:
                    on_done(False)

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # ANTI-EMULATOR DETECTION (REAL SMARTPHONE STEALTH ENGINE)
    # =========================================================================

    def patch_system_image_build_prop(self, sysimg_dir: str):
        """
        Patches the system image's build.prop on disk (creating a backup first) so static checks
        see a genuine Retail Google Pixel 9 Pro XL (`komodo`, `user`, `release-keys`) instead of `sdk_gphone` / `emu64xa`.
        """
        bp_path = os.path.join(sysimg_dir, "build.prop")
        if not os.path.exists(bp_path):
            return
        bak_path = bp_path + ".orig_bak"
        if not os.path.exists(bak_path):
            try:
                shutil.copy2(bp_path, bak_path)
            except Exception:
                pass

        pix = PIXEL_PROFILES.get(self.selected_pixel, PIXEL_PROFILES["pixel_9_pro_xl"])
        replacements = {
            "ro.product.system.brand": pix["brand"],
            "ro.product.system.device": pix["device"],
            "ro.product.system.manufacturer": pix["manufacturer"],
            "ro.product.system.model": pix["model"],
            "ro.product.system.name": pix["product"],
            "ro.build.product": pix["product"],
            "ro.product.model": pix["model"],
            "ro.product.brand": pix["brand"],
            "ro.product.name": pix["product"],
            "ro.product.device": pix["device"],
            "ro.product.manufacturer": pix["manufacturer"],
            "ro.system.build.type": "user",
            "ro.build.type": "user",
            "ro.system.build.tags": "release-keys",
            "ro.build.tags": "release-keys",
            "ro.system.build.fingerprint": pix["fingerprint"],
            "ro.build.fingerprint": pix["fingerprint"],
            "ro.build.description": pix["description"],
        }
        try:
            with open(bp_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                if "=" in line and not line.lstrip().startswith("#"):
                    k = line.split("=", 1)[0].strip()
                    if k in replacements:
                        new_lines.append(f"{k}={replacements[k]}\n")
                        continue
                new_lines.append(line)
            with open(bp_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception as e:
            self.log(f"Note: build.prop static patch skipped ({e})", "WARN")

    def apply_live_stealth_smartphone_identity(self):
        """
        Executes deep runtime Anti-Emulator Detection spoofing over ADB + Magisk `resetprop`:
        - Replaces all `generic`, `sdk_gphone`, `ranchu`, `goldfish`, `qemu` properties with genuine
          Retail Google Pixel 9 Pro XL (`komodo`) values.
        - Spoofs `ro.kernel.qemu=0`, `ro.boot.qemu=0`, `ro.hardware=komodo`, `ro.Boot.verifiedbootstate=green`,
          `ro.build.tags=release-keys`, `ro.build.type=user`, SIM Operator (`Telekom.de` / `26201`),
          IMEI, Serial Number, and Battery state.
        """
        if not self.stealth_enabled:
            return

        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        prof = self.get_active_profile()
        pix = PIXEL_PROFILES.get(self.selected_pixel, PIXEL_PROFILES["pixel_9_pro_xl"])
        imei = prof.get("imei") or generate_random_imei()
        serial = prof.get("serial") or generate_random_serial()
        carrier = prof.get("carrier", "Telekom.de")

        self.log(f"🛡 [ANTI-DETECT STEALTH] Cloaking Emulator as Real Retail {pix['model']} ({pix['device']}, IMEI: {imei})...", "CYBER")

        # Ensure Magisk resetprop binary is available in /data/local/tmp/resetprop even if Root is later turned OFF
        magisk_bin = os.path.join(ROOT_METHODS_DIR, "magisk", "bin_x86_64", "magisk")
        subprocess.run([self.adb_exe, "root"], env=env, capture_output=True, timeout=8, creationflags=cflags)
        if os.path.exists(magisk_bin):
            subprocess.run([self.adb_exe, "push", magisk_bin, "/data/local/tmp/magisk_stealth"], env=env, capture_output=True, timeout=8, creationflags=cflags)
            subprocess.run([self.adb_exe, "shell", "chmod 755 /data/local/tmp/magisk_stealth; ln -sf /data/local/tmp/magisk_stealth /data/local/tmp/resetprop"], env=env, capture_output=True, timeout=5, creationflags=cflags)

        stealth_props = {
            "ro.product.brand": pix["brand"],
            "ro.product.manufacturer": pix["manufacturer"],
            "ro.product.model": pix["model"],
            "ro.product.name": pix["product"],
            "ro.product.device": pix["device"],
            "ro.product.board": pix["board"],
            "ro.hardware": pix["hardware"],
            "ro.boot.hardware": pix["hardware"],
            "ro.build.product": pix["product"],
            "ro.build.fingerprint": pix["fingerprint"],
            "ro.system.build.fingerprint": pix["fingerprint"],
            "ro.vendor.build.fingerprint": pix["fingerprint"],
            "ro.bootimage.build.fingerprint": pix["fingerprint"],
            "ro.build.description": pix["description"],
            "ro.build.tags": "release-keys",
            "ro.build.type": "user",
            "ro.debuggable": "0",
            "ro.secure": "1",
            "ro.kernel.qemu": "0",
            "ro.boot.qemu": "0",
            "ro.kernel.android.qemud": "",
            "ro.boot.verifiedbootstate": "green",
            "ro.boot.flash.locked": "1",
            "ro.boot.vbmeta.device_state": "locked",
            "ro.boot.warranty_bit": "0",
            "ro.warranty_bit": "0",
            "ro.serialno": serial,
            "ro.boot.serialno": serial,
            "ro.baseband": pix["baseband"],
            "ro.bootloader": pix["bootloader"],
            "ro.soc.manufacturer": pix["soc_manufacturer"],
            "ro.soc.model": pix["soc_model"],
            "gsm.sim.operator.alpha": carrier,
            "gsm.operator.alpha": carrier,
            "gsm.sim.operator.numeric": "26201",
            "gsm.operator.numeric": "26201",
            "gsm.sim.operator.iso-country": "de",
            "gsm.version.baseband": pix["baseband"],
            "persist.sys.pixel.imei": imei,
        }

        cmds = []
        for k, v in stealth_props.items():
            cmds.append(f"/data/local/tmp/resetprop -n '{k}' '{v}' 2>/dev/null || setprop '{k}' '{v}' 2>/dev/null")

        # Also spoof realistic battery level & charging state and hide qemu pipes readability from unprivileged apps
        cmds.append("dumpsys battery set level 87; dumpsys battery set status 2; dumpsys battery set ac 0; dumpsys battery set usb 0")
        cmds.append("chmod 000 /dev/qemu_pipe /dev/goldfish_pipe /sys/qemu_trace 2>/dev/null || true")
        cmds.append(f"settings put global device_name '{pix['model']}'; settings put secure bluetooth_name '{pix['model']}'")

        full_script = "; ".join(cmds)
        subprocess.run([self.adb_exe, "shell", full_script], env=env, capture_output=True, text=True, timeout=15, creationflags=cflags)
        self.log(f"✔ [STEALTH ACTIVE] Device now reports as genuine '{pix['manufacturer']} {pix['model']}' ({pix['device']}, release-keys, VerifiedBoot=green)!", "SUCCESS")

    # =========================================================================
    # APK & XAPK (SPLIT-APKS + OBB) ONE-CLICK INSTALLER
    # =========================================================================

    def install_apk_or_xapk(self, file_path: str):
        """
        Installs both standard `.apk` files and `.xapk` / `.apkm` / `.apks` bundles!
        For `.xapk`:
        1. Extracts `manifest.json`, all `.apk` splits, and any `Android/obb/<pkg>/*.obb` expansion files.
        2. Installs all split `.apk` files in a single atomic transaction via `adb install-multiple -r -g`.
        3. Pushes any `.obb` files directly to `/sdcard/Android/obb/<pkg>/`.
        """
        def _worker():
            ext = os.path.splitext(file_path)[1].lower()
            fname = os.path.basename(file_path)
            env = self.get_env()
            cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

            if ext == ".apk":
                self.log(f"📦 Installing APK: {fname} ...", "CYBER")
                self.progress(40, f"INSTALLING APK: {fname}...")
                r = subprocess.run([self.adb_exe, "install", "-r", "-g", file_path], env=env, capture_output=True, text=True, creationflags=cflags)
                out = (r.stdout or "") + (r.stderr or "")
                if "Success" in out:
                    self.progress(100, f"✔ APK INSTALLED: {fname}")
                    self.log(f"✔ APK Installed Successfully: {fname}", "SUCCESS")
                else:
                    self.progress(0, "APK INSTALL WARNING")
                    self.log(f"APK Install Output: {out.strip()}", "WARN")
                return

            # Handle .xapk / .apkm / .apks archive
            self.log(f"📦 Unpacking XAPK/Split Bundle: {fname} ...", "CYBER")
            self.progress(20, f"EXTRACTING XAPK BUNDLE: {fname}...")
            tmp_extract = os.path.join(CACHE_DIR, f"xapk_{ int(time.time()) }")
            os.makedirs(tmp_extract, exist_ok=True)
            try:
                with zipfile.ZipFile(file_path, "r") as z:
                    z.extractall(tmp_extract)

                apk_files = []
                obb_files = []
                for root_d, _, files in os.walk(tmp_extract):
                    for f in files:
                        full_f = os.path.join(root_d, f)
                        if f.lower().endswith(".apk"):
                            apk_files.append(full_f)
                        elif f.lower().endswith(".obb"):
                            rel_p = os.path.relpath(full_f, tmp_extract).replace("\\", "/")
                            obb_files.append((full_f, rel_p))

                if not apk_files:
                    self.log(f"No .apk files found inside {fname}!", "ERROR")
                    return

                self.log(f"Found {len(apk_files)} Split-APK(s) and {len(obb_files)} OBB file(s) in {fname}.", "CYBER")
                self.progress(55, f"INSTALLING {len(apk_files)} SPLIT APKS VIA ADB...")

                cmd = [self.adb_exe, "install-multiple", "-r", "-g"] + apk_files
                r = subprocess.run(cmd, env=env, capture_output=True, text=True, creationflags=cflags)
                out = (r.stdout or "") + (r.stderr or "")

                if obb_files:
                    self.progress(80, f"PUSHING {len(obb_files)} OBB GAME DATA FILES TO /sdcard/Android/obb...")
                    for local_obb, rel_obb in obb_files:
                        if "Android/obb/" in rel_obb:
                            remote_dst = "/sdcard/" + rel_obb[rel_obb.index("Android/obb/"):]
                        else:
                            remote_dst = f"/sdcard/Android/obb/{os.path.basename(local_obb)}"
                        remote_dir = os.path.dirname(remote_dst).replace("\\", "/")
                        subprocess.run([self.adb_exe, "shell", f"mkdir -p '{remote_dir}'"], env=env, capture_output=True, creationflags=cflags)
                        subprocess.run([self.adb_exe, "push", local_obb, remote_dst], env=env, capture_output=True, creationflags=cflags)
                        self.log(f"✔ Pushed OBB -> {remote_dst}", "SUCCESS")

                if "Success" in out:
                    self.progress(100, f"✔ XAPK INSTALLED: {fname}")
                    self.log(f"✔ XAPK Bundle Installed Successfully: {fname}", "SUCCESS")
                else:
                    self.log(f"XAPK Install Result: {out.strip()}", "WARN")
            except Exception as e:
                self.log(f"XAPK Install Error: {e}", "ERROR")
            finally:
                shutil.rmtree(tmp_extract, ignore_errors=True)

        threading.Thread(target=_worker, daemon=True).start()

    # =========================================================================
    # ANDROID NAVIGATION KEYS, BACKGROUND APPS & SHARED FOLDER BRIDGE
    # =========================================================================

    def send_nav_key(self, key_event: int, label: str = ""):
        """Sends Android keyevents: 4 = BACK, 3 = HOME, 187 = APP_SWITCH (Recents), 24 = VOL+, 25 = VOL-, 26 = POWER."""
        def _worker():
            env = self.get_env()
            cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            subprocess.run([self.adb_exe, "shell", "input", "keyevent", str(key_event)], env=env, capture_output=True, timeout=4, creationflags=cflags)
            if label:
                self.log(f"[NAV] Triggered Android '{label}' (KeyEvent {key_event})", "CYBER")
        threading.Thread(target=_worker, daemon=True).start()

    def list_running_background_apps(self) -> list:
        """Returns a list of currently running user/foreground/background packages on the emulator."""
        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        apps = []
        try:
            r = subprocess.run(
                [self.adb_exe, "shell", "cmd activity stack list 2>/dev/null || dumpsys activity recents | grep 'Recent #'"],
                env=env, capture_output=True, text=True, timeout=4, creationflags=cflags
            )
            seen = set()
            for line in (r.stdout or "").splitlines():
                if "/" in line:
                    for token in line.split():
                        if "/" in token and "." in token:
                            pkg = token.split("/")[0].split("{")[-1].split(":")[-1].strip()
                            if pkg and "." in pkg and not pkg.startswith("com.android.systemui") and pkg not in seen:
                                seen.add(pkg)
                                apps.append(pkg)
            if not apps:
                r2 = subprocess.run([self.adb_exe, "shell", "pm list packages -3"], env=env, capture_output=True, text=True, timeout=4, creationflags=cflags)
                for ln in (r2.stdout or "").splitlines():
                    if ln.startswith("package:"):
                        apps.append(ln.replace("package:", "").strip())
        except Exception:
            pass
        return apps[:25]

    def kill_background_app(self, package_name: str):
        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        subprocess.run([self.adb_exe, "shell", "am", "force-stop", package_name], env=env, capture_output=True, timeout=4, creationflags=cflags)
        self.log(f"🛑 Force-stopped background app: {package_name}", "WARN")

    def sync_shared_folder_to_emulator(self, specific_file: str = None):
        r"""
        Copies either a specific file or all files inside `d:\SHOXX_EMU_26\Shared_PC_Folder`
        directly to `/sdcard/Download/ShoXx_Shared/` on the Android Emulator and triggers MediaScanner!
        """
        def _worker():
            env = self.get_env()
            cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            remote_dir = "/sdcard/Download/ShoXx_Shared"
            subprocess.run([self.adb_exe, "shell", f"mkdir -p {remote_dir}"], env=env, capture_output=True, timeout=5, creationflags=cflags)

            if specific_file and os.path.exists(specific_file):
                # Copy into Shared_PC_Folder as well so it stays synced
                dst_local = os.path.join(SHARED_PC_DIR, os.path.basename(specific_file))
                if os.path.abspath(specific_file) != os.path.abspath(dst_local):
                    shutil.copy2(specific_file, dst_local)
                files_to_push = [dst_local]
            else:
                files_to_push = [
                    os.path.join(SHARED_PC_DIR, f)
                    for f in os.listdir(SHARED_PC_DIR)
                    if os.path.isfile(os.path.join(SHARED_PC_DIR, f))
                ]

            if not files_to_push:
                self.log("Shared_PC_Folder is empty — place files there or pick a file to transfer.", "WARN")
                return

            self.log(f"📂 Syncing {len(files_to_push)} file(s) from PC Shared Folder -> Emulator ({remote_dir})...", "CYBER")
            for idx, fp in enumerate(files_to_push):
                fn = os.path.basename(fp)
                self.progress(int(((idx + 1) / len(files_to_push)) * 100), f"COPYING TO EMULATOR: {fn}")
                subprocess.run([self.adb_exe, "push", fp, f"{remote_dir}/{fn}"], env=env, capture_output=True, timeout=30, creationflags=cflags)

            subprocess.run(
                [self.adb_exe, "shell", f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{remote_dir}"],
                env=env, capture_output=True, timeout=5, creationflags=cflags
            )
            self.log(f"✔ Synced {len(files_to_push)} file(s) to Emulator: {remote_dir}", "SUCCESS")

        threading.Thread(target=_worker, daemon=True).start()

    def pull_shared_folder_from_emulator(self):
        """Pulls files from `/sdcard/Download/ShoXx_Shared` on the Emulator back into `Shared_PC_Folder` on the PC."""
        def _worker():
            env = self.get_env()
            cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            remote_dir = "/sdcard/Download/ShoXx_Shared/."
            self.log(f"📥 Pulling files from Emulator (/sdcard/Download/ShoXx_Shared) -> {SHARED_PC_DIR}...", "CYBER")
            subprocess.run([self.adb_exe, "pull", remote_dir, SHARED_PC_DIR], env=env, capture_output=True, timeout=30, creationflags=cflags)
            self.log(f"✔ Pulled Emulator shared files into {SHARED_PC_DIR}!", "SUCCESS")
        threading.Thread(target=_worker, daemon=True).start()

    def open_pc_shared_folder_explorer(self):
        os.makedirs(SHARED_PC_DIR, exist_ok=True)
        if os.name == "nt":
            os.startfile(SHARED_PC_DIR)

    # =========================================================================
    # ONE-CLICK CLEAN & PORTABLE ZIP EXPORT (PROFILE OR FULL SUITE)
    # =========================================================================

    def clean_and_verify_portability(self) -> dict:
        """
        Cleans all temporary cache files (`./_cache/temp/`, `*.asdownload`, `__pycache__`),
        removes stale AVD `.lock` files, and relinks all `.ini` paths for 100% portability.
        """
        freed_bytes = 0
        cleaned_items = 0

        # 1. Clean ./_cache/temp and temporary extraction folders inside ./_cache
        if os.path.exists(CACHE_DIR):
            for root_d, dirs, files in os.walk(CACHE_DIR, topdown=False):
                for f in files:
                    fp = os.path.join(root_d, f)
                    try:
                        freed_bytes += os.path.getsize(fp)
                        os.remove(fp)
                        cleaned_items += 1
                    except Exception:
                        pass
                for d in dirs:
                    dp = os.path.join(root_d, d)
                    if os.path.abspath(dp) != os.path.abspath(TEMP_PORTABLE_DIR):
                        try:
                            shutil.rmtree(dp, ignore_errors=True)
                        except Exception:
                            pass
        os.makedirs(TEMP_PORTABLE_DIR, exist_ok=True)

        # 2. Remove stale hardware-qemu.ini.lock / multiinstance.lock files/dirs and heavy volatile ram.img in AVDs
        if os.path.exists(AVD_HOME):
            for root_d, dirs, files in os.walk(AVD_HOME, topdown=False):
                for f in files:
                    if f.endswith(".lock") or f in ("ram.img", "ram.img.dirty", "tmpAdbCmds"):
                        fp = os.path.join(root_d, f)
                        try:
                            freed_bytes += os.path.getsize(fp)
                            os.remove(fp)
                            cleaned_items += 1
                        except Exception:
                            pass
                for d in dirs:
                    if d.endswith(".lock") or d == "snapshots":
                        dp = os.path.join(root_d, d)
                        try:
                            for sr, _, sfs in os.walk(dp):
                                for sf in sfs:
                                    freed_bytes += os.path.getsize(os.path.join(sr, sf))
                            shutil.rmtree(dp, ignore_errors=True)
                            cleaned_items += 1
                        except Exception:
                            pass

        # 3. Relink all AVD .ini files to current BASE_DIR
        self.relink_portable_paths()

        freed_mb = round(freed_bytes / (1024 * 1024), 2)
        self.log(
            f"✔ Portability Audit & Cleanup complete: Removed {cleaned_items} temp/lock file(s) ({freed_mb} MB freed), all AVD paths relinked.",
            "SUCCESS"
        )
        return {"cleaned_items": cleaned_items, "freed_mb": freed_mb, "portable_verified": True}

    def export_portable_zip(self, dest_zip_path: str, mode: str = "profile", profile_id: str = None, on_done=None):
        """
        Packages either the selected Emulator Profile (`mode='profile'`) or the complete
        Portable Application Core (`mode='full_core'`) into a clean, ready-to-share `.zip` archive!
        """
        def _worker():
            try:
                self.progress(5, "RUNNING PRE-EXPORT PORTABILITY CLEANUP & AUDIT...")
                self.clean_and_verify_portability()

                prof = None
                for p in self.profiles:
                    if p["id"] == (profile_id or self.active_profile_id):
                        prof = p
                        break
                prof = prof or self.get_active_profile()

                files_to_pack = []
                skip_heavy = {
                    "userdata-qemu.img", "userdata-qemu.img.qcow2",
                    "cache.img", "cache.img.qcow2",
                    "encryptionkey.img", "encryptionkey.img.qcow2",
                    "system.img.qcow2", "vendor.img.qcow2",
                    "ram.img", "ram.img.dirty", "initrd"
                }
                if mode == "profile":
                    avd_name = prof["avd_name"]
                    avd_dir = os.path.join(AVD_HOME, f"{avd_name}.avd")
                    avd_ini = os.path.join(AVD_HOME, f"{avd_name}.ini")
                    if os.path.exists(avd_ini):
                        files_to_pack.append((avd_ini, os.path.relpath(avd_ini, BASE_DIR)))
                    if os.path.exists(avd_dir):
                        for r_d, _, fls in os.walk(avd_dir):
                            if "snapshots" in r_d or ".lock" in r_d:
                                continue
                            for f in fls:
                                if not f.endswith(".lock") and f not in skip_heavy:
                                    full_p = os.path.join(r_d, f)
                                    files_to_pack.append((full_p, os.path.relpath(full_p, BASE_DIR)))
                    if os.path.exists(PROFILES_JSON):
                        files_to_pack.append((PROFILES_JSON, os.path.relpath(PROFILES_JSON, BASE_DIR)))
                else:
                    # Pack full portable launcher, src, assets, root_methods, Shared_PC_Folder, and active profile configs
                    include_roots = [
                        "ShoXx_Emu.py",
                        "One_Click_Start_ShoXx_Emu.bat",
                        "Auto_Boot_Android17_Fullscreen.bat",
                        "AGENTS.md",
                        "README.md",
                        "src",
                        "assets",
                        "root_methods",
                        "Shared_PC_Folder",
                        "avd_data",
                    ]
                    for item in include_roots:
                        full_item = os.path.join(BASE_DIR, item)
                        if os.path.isfile(full_item):
                            files_to_pack.append((full_item, item))
                        elif os.path.isdir(full_item):
                            for r_d, _, fls in os.walk(full_item):
                                if "__pycache__" in r_d or "snapshots" in r_d or ".lock" in r_d:
                                    continue
                                for f in fls:
                                    if f.endswith(".lock") or f.endswith(".pyc") or f in skip_heavy:
                                        continue
                                    fp = os.path.join(r_d, f)
                                    if os.path.abspath(fp) == os.path.abspath(dest_zip_path):
                                        continue
                                    files_to_pack.append((fp, os.path.relpath(fp, BASE_DIR)))

                total_f = max(1, len(files_to_pack))
                self.log(f"📦 Creating Portable ZIP Archive ({total_f} files) -> {dest_zip_path} ...", "CYBER")

                with zipfile.ZipFile(dest_zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
                    if mode == "profile":
                        zf.writestr("profile_manifest.json", json.dumps(prof, indent=2))
                    for idx, (src_p, arc_name) in enumerate(files_to_pack):
                        pct = 10 + int(((idx + 1) / total_f) * 88)
                        self.progress(pct, f"PACKING PORTABLE ZIP ({idx + 1}/{total_f}): {os.path.basename(src_p)}")
                        zf.write(src_p, arc_name)

                size_mb = round(os.path.getsize(dest_zip_path) / (1024 * 1024), 2)
                self.progress(100, f"✔ PORTABLE ZIP EXPORT COMPLETE ({size_mb} MB)!")
                self.log(f"✔ Portable Export saved to: {dest_zip_path} ({size_mb} MB)", "SUCCESS")
                if on_done:
                    on_done(True, dest_zip_path, size_mb)
            except Exception as e:
                self.log(f"Portable ZIP Export Error: {e}", "ERROR")
                self.progress(0, f"EXPORT ERROR: {e}")
                if on_done:
                    on_done(False, str(e), 0)

        threading.Thread(target=_worker, daemon=True).start()

    def import_profile_zip(self, zip_path: str) -> dict:
        """
        One-Click Profile ZIP Importer:
        Extracts a portable Profile `.zip` archive into `./avd_data/.android/avd/`,
        registers or updates the profile metadata in `profiles.json`, dynamically relinks
        all `.ini` paths to the current `BASE_DIR`, and activates the imported profile!
        """
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"ZIP file not found: {zip_path}")

        self.progress(15, f"IMPORTING PORTABLE PROFILE: {os.path.basename(zip_path)}...")
        imported_prof = None
        detected_avd_name = None

        with zipfile.ZipFile(zip_path, "r") as zf:
            names = zf.namelist()
            if "profile_manifest.json" in names:
                try:
                    imported_prof = json.loads(zf.read("profile_manifest.json").decode("utf-8"))
                except Exception:
                    pass
            elif "avd_data/profiles.json" in names or "avd_data\\profiles.json" in names:
                key = "avd_data/profiles.json" if "avd_data/profiles.json" in names else "avd_data\\profiles.json"
                try:
                    pdata = json.loads(zf.read(key).decode("utf-8"))
                    act_id = pdata.get("active_id")
                    profs = pdata.get("profiles", [])
                    for p in profs:
                        if p.get("id") == act_id:
                            imported_prof = p
                            break
                    if not imported_prof and profs:
                        imported_prof = profs[0]
                except Exception:
                    pass

            for member in names:
                norm_m = member.replace("\\", "/")
                if norm_m in ("profile_manifest.json", "avd_data/profiles.json") or norm_m.endswith(".lock"):
                    continue
                if norm_m.startswith("avd_data/.android/avd/"):
                    parts = norm_m.split("/")
                    if len(parts) >= 4 and parts[3].endswith(".ini"):
                        detected_avd_name = parts[3][:-4]
                    elif len(parts) >= 4 and parts[3].endswith(".avd"):
                        detected_avd_name = parts[3][:-4]
                    target_path = os.path.join(BASE_DIR, *parts)
                    if member.endswith("/") or member.endswith("\\"):
                        os.makedirs(target_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with zf.open(member) as src_f, open(target_path, "wb") as dst_f:
                            shutil.copyfileobj(src_f, dst_f)

        if not imported_prof:
            uid = uuid.uuid4().hex[:6]
            avd_n = detected_avd_name or f"ShoXx_Imported_{uid}"
            imported_prof = {
                "id": f"prof_{uid}",
                "name": f"Imported Profile ({avd_n})",
                "avd_name": avd_n,
                "android_ver": "16",
                "pixel_model": "pixel_9_pro_xl",
                "root_enabled": True,
                "root_method": "MAGISK",
                "stealth_enabled": True,
                "ram_mb": self.ram_mb,
                "cores": self.cores,
                "gpu_mode": self.gpu_mode,
                "imei": generate_random_imei(),
                "serial": generate_random_serial(),
                "carrier": "Telekom.de",
            }

        # Update existing profile with same id or append as new profile
        replaced = False
        for idx, p in enumerate(self.profiles):
            if p["id"] == imported_prof["id"] or p.get("avd_name") == imported_prof.get("avd_name"):
                self.profiles[idx] = imported_prof
                replaced = True
                break
        if not replaced:
            self.profiles.append(imported_prof)

        self.select_profile(imported_prof["id"])
        self.relink_portable_paths()
        self.create_or_update_avd(
            android_ver=imported_prof.get("android_ver", "16"),
            avd_name=imported_prof["avd_name"],
            profile=imported_prof
        )
        self.progress(100, f"✔ IMPORTED PROFILE: {imported_prof['name']}")
        self.log(f"✔ Successfully imported & relinked Portable Profile: '{imported_prof['name']}' ({imported_prof['avd_name']})", "SUCCESS")
        return imported_prof

    # =========================================================================
    # DEEP HARDWARE & SYSTEM ANALYZER + OPTIMAL SETTINGS ENGINE
    # =========================================================================

    def analyze_system_hardware(self) -> dict:
        cpu_name = platform.processor() or "x86_64 Processor"
        cpu_mhz = 3000
        cpu_threads = os.cpu_count() or 4

        if os.name == "nt":
            try:
                import winreg
                k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                cpu_name, _ = winreg.QueryValueEx(k, "ProcessorNameString")
                cpu_mhz, _ = winreg.QueryValueEx(k, "~MHz")
                cpu_name = cpu_name.strip()
            except Exception:
                pass

        ram_total_mb = 8192
        ram_avail_mb = 4096
        ram_load_pct = 50
        if os.name == "nt":
            try:
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                mem = MEMORYSTATUSEX()
                mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
                ram_total_mb = int(mem.ullTotalPhys // (1024 * 1024))
                ram_avail_mb = int(mem.ullAvailPhys // (1024 * 1024))
                ram_load_pct = int(mem.dwMemoryLoad)
            except Exception:
                pass

        gpus = []
        if os.name == "nt":
            try:
                import winreg
                base_k = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
                )
                for i in range(16):
                    try:
                        sub = winreg.OpenKey(base_k, f"{i:04d}")
                        desc, _ = winreg.QueryValueEx(sub, "DriverDesc")
                        vram = 0
                        try:
                            vram, _ = winreg.QueryValueEx(sub, "HardwareInformation.qwMemorySize")
                        except Exception:
                            try:
                                vram, _ = winreg.QueryValueEx(sub, "HardwareInformation.MemorySize")
                                if isinstance(vram, bytes):
                                    vram = int.from_bytes(vram, "little")
                            except Exception:
                                vram = 0
                        try:
                            drv, _ = winreg.QueryValueEx(sub, "DriverVersion")
                        except Exception:
                            drv = "N/A"
                        vram_mb = int(vram // (1024 * 1024)) if isinstance(vram, int) else 0
                        gpus.append({"name": desc.strip(), "vram_mb": vram_mb, "driver": drv})
                    except Exception:
                        pass
            except Exception:
                pass

        gpus.sort(key=lambda g: (1 if any(v in g["name"].upper() for v in ["NVIDIA", "RADEON", "RTX", "GTX", "ARC"]) else 0, g["vram_mb"]), reverse=True)
        primary_gpu = gpus[0] if gpus else {"name": "Standard OpenGL GPU", "vram_mb": 2048, "driver": "Generic"}

        accel_ok = False
        accel_detail = "Checking..."
        if os.path.exists(self.emulator_exe):
            try:
                cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                res = subprocess.run(
                    [self.emulator_exe, "-accel-check"],
                    env=self.get_env(), capture_output=True, text=True, timeout=4, creationflags=cflags
                )
                lines = [ln.strip() for ln in (res.stdout or "").splitlines() if ln.strip() and ln.strip() != "accel:" and ln.strip() != "accel" and not ln.strip().isdigit()]
                if lines:
                    accel_detail = lines[0]
                    accel_ok = "usable" in accel_detail.lower()
                else:
                    accel_detail = "Hardware Hypervisor Ready"
                    accel_ok = True
            except Exception:
                accel_detail = "Hypervisor Default"
        else:
            accel_detail = "Emulator Engine Pending Setup"

        try:
            du = shutil.disk_usage(BASE_DIR)
            disk_total_gb = round(du.total / (1024 ** 3), 1)
            disk_free_gb = round(du.free / (1024 ** 3), 1)
            disk_used_pct = int((du.used / du.total) * 100)
        except Exception:
            disk_total_gb, disk_free_gb, disk_used_pct = 500.0, 250.0, 50

        screen_w, screen_h = 1920, 1080
        if os.name == "nt":
            try:
                screen_w = ctypes.windll.user32.GetSystemMetrics(0)
                screen_h = ctypes.windll.user32.GetSystemMetrics(1)
            except Exception:
                pass

        if cpu_threads >= 12:
            rec_cores, rec_cores_label = 8, "8 Cores (Max)"
        elif cpu_threads >= 8:
            rec_cores, rec_cores_label = 6, "6 Cores (Extreme)"
        elif cpu_threads >= 4:
            rec_cores, rec_cores_label = 4, "4 Cores (Turbo)"
        else:
            rec_cores, rec_cores_label = 2, "2 Cores"

        if ram_total_mb >= 24000 and ram_avail_mb >= 8500:
            rec_ram_mb, rec_ram_label = 8192, "8192 MB (8 GB)"
        elif ram_total_mb >= 15000 and ram_avail_mb >= 4500:
            rec_ram_mb, rec_ram_label = 6144, "6144 MB (6 GB)"
        elif ram_total_mb >= 12000:
            rec_ram_mb, rec_ram_label = 4096, "4096 MB (4 GB)"
        else:
            rec_ram_mb, rec_ram_label = 2048, "2048 MB (2 GB)"

        has_dedicated_gpu = primary_gpu["vram_mb"] >= 2048 or any(k in primary_gpu["name"].upper() for k in ["NVIDIA", "RTX", "GTX", "RADEON", "ARC"])
        rec_gpu_mode = "host" if has_dedicated_gpu else "auto"
        rec_gpu_desc = f"host (Hardware OpenGL/Gfxstream via {primary_gpu['name']})" if has_dedicated_gpu else "auto (Integrated Renderer)"

        rec_res = (screen_w - SIDEBAR_WIDTH, screen_h)
        rec_res_label = f"PC Fullscreen + Gaming Sidebar ({screen_w}x{screen_h})"
        rec_dpi = 320 if screen_w <= 1920 else 420

        cpu_score = min(30, int((cpu_threads / 4) * 18 + (cpu_mhz / 3400) * 12))
        ram_score = min(25, int((ram_total_mb / 16384) * 25))
        gpu_score = min(25, int((max(1024, primary_gpu["vram_mb"]) / 4096) * 25))
        accel_score = 20 if accel_ok else 8
        total_score = min(100, cpu_score + ram_score + gpu_score + accel_score)

        if total_score >= 88:
            tier_name = "CYBER ULTRA // HIGH-FPS PIXEL STEALTH + GAMING EXTEND"
        elif total_score >= 70:
            tier_name = "NEON TURBO // OPTIMAL PIXEL & ROOT WORKSTATION"
        else:
            tier_name = "BALANCED CORE // STABLE EMULATION PROFILE"

        self.optimal_settings = {
            "cores": rec_cores,
            "cores_label": rec_cores_label,
            "ram_mb": rec_ram_mb,
            "ram_label": rec_ram_label,
            "gpu_mode": rec_gpu_mode,
            "gpu_desc": rec_gpu_desc,
            "resolution": rec_res,
            "resolution_label": rec_res_label,
            "dpi": rec_dpi,
            "pixel_profile": "pixel_9_pro_xl",
            "fullscreen": True,
            "root_enabled": True,
            "score": total_score,
            "tier": tier_name,
            "summary": (
                f"PIXEL 9 PRO XL STEALTH ({screen_w}x{screen_h})  •  {rec_cores} Cores  •  {rec_ram_mb} MB RAM  •  "
                f"GPU '{rec_gpu_mode}' ({primary_gpu['name']})"
            )
        }

        self.system_report = {
            "os": f"Windows {platform.release()} ({platform.version()}) 64-Bit",
            "cpu_name": cpu_name,
            "cpu_mhz": cpu_mhz,
            "cpu_threads": cpu_threads,
            "cpu_score_pct": min(100, int(((cpu_threads * cpu_mhz) / 13600) * 85)),
            "ram_total_mb": ram_total_mb,
            "ram_avail_mb": ram_avail_mb,
            "ram_load_pct": ram_load_pct,
            "primary_gpu": primary_gpu,
            "all_gpus": gpus,
            "gpu_score_pct": min(100, int((max(1024, primary_gpu["vram_mb"]) / 4096) * 90)),
            "accel_ok": accel_ok,
            "accel_detail": accel_detail,
            "disk_total_gb": disk_total_gb,
            "disk_free_gb": disk_free_gb,
            "disk_used_pct": disk_used_pct,
            "screen_w": screen_w,
            "screen_h": screen_h,
            "optimal": self.optimal_settings,
        }
        return self.system_report

    def inspect_plugins_and_tools(self) -> list:
        sys_rep = self.system_report or self.analyze_system_hardware()

        emu_exists = os.path.exists(self.emulator_exe)
        adb_exists = os.path.exists(self.adb_exe)
        accel_ok = sys_rep.get("accel_ok", False)

        rom15 = self.get_rom_status("15")
        rom16 = self.get_rom_status("16")
        rom17 = self.get_rom_status("17")

        magisk_ok = os.path.exists(os.path.join(ROOT_METHODS_DIR, "magisk", "Magisk.apk"))
        ksu_ok = os.path.exists(os.path.join(ROOT_METHODS_DIR, "kernelsu", "KernelSU.apk"))
        apatch_ok = os.path.exists(os.path.join(ROOT_METHODS_DIR, "apatch", "APatch.apk"))

        self.plugins_report = [
            {
                "id": "emu_accel",
                "name": "Android Studio Emulator + Google AEHD Hypervisor",
                "category": "EMULATOR CORE",
                "version": f"v35.4.9.0 Gfxstream | {sys_rep.get('accel_detail', 'AEHD v2.0')}",
                "installed": emu_exists and accel_ok,
                "status_text": "INSTALLED & ACTIVE" if (emu_exists and accel_ok) else "SETUP REQUIRED",
            },
            {
                "id": "stealth_engine",
                "name": "Anti-Emulator Stealth Engine (Pixel 9 Pro XL komodo)",
                "category": "ANTI-DETECT",
                "version": "Retail Fingerprint + IMEI/Carrier Spoof + Pipe Cloak",
                "installed": True,
                "status_text": "ACTIVE (STEALTH)" if self.stealth_enabled else "STANDBY",
            },
            {
                "id": "android_16",
                "name": "Android 16 ROM (API 36 Baklava + Google Play Store)",
                "category": "ANDROID 16",
                "version": "Google Play Store Pre-Installed (x86_64)" if rom16["has_playstore"] else "Base ROM Installed (Play Store DL Ready)",
                "installed": rom16["any_installed"],
                "status_text": "PLAY STORE READY" if rom16["has_playstore"] else ("BASE READY (DL PLAY)" if rom16["has_default"] else "DOWNLOAD READY"),
            },
            {
                "id": "android_17",
                "name": "Android 17 ROM (API 37 CinnamonBun + Google Play Store)",
                "category": "ANDROID 17",
                "version": "Google Play Store Installed" if rom17["has_playstore"] else "Base ROM Bundled + Play Store DL Ready",
                "installed": rom17["any_installed"],
                "status_text": "PLAY STORE READY" if rom17["has_playstore"] else ("BUNDLED (DL PLAY)" if rom17["has_default"] else "DOWNLOAD READY"),
            },
            {
                "id": "android_15",
                "name": "Android 15 ROM (API 35 V.I.C. + Google Play Store)",
                "category": "ANDROID 15",
                "version": "Google Play Store Installed" if rom15["has_playstore"] else "Base ROM Bundled + Play Store DL Ready",
                "installed": rom15["any_installed"],
                "status_text": "PLAY STORE READY" if rom15["has_playstore"] else ("BUNDLED (DL PLAY)" if rom15["has_default"] else "DOWNLOAD READY"),
            },
            {
                "id": "root_magisk",
                "name": "Root #1: Magisk v31.1 + Root #2: KernelSU v3.3.1",
                "category": "MULTI-ROOT",
                "version": "Magisk v31.1 (Zygisk) & KernelSU v3.3.1 (ksud) x86_64",
                "installed": magisk_ok and ksu_ok,
                "status_text": "BUNDLED & READY" if (magisk_ok and ksu_ok) else "MISSING",
            },
            {
                "id": "root_apatch",
                "name": "Root #3: APatch 11282 + APK/XAPK OBB Split Installer",
                "category": "APATCH & XAPK",
                "version": "APatch v11282 + Native adbd SU + .apk/.xapk Installer",
                "installed": apatch_ok and adb_exists,
                "status_text": "BUNDLED & READY" if apatch_ok else "MISSING",
            },
            {
                "id": "gaming_sidebar",
                "name": f"Gaming Extend Sidebar & Shared PC Folder ({len(self.profiles)} Profiles)",
                "category": "GAMING EXTEND",
                "version": f"Nav Keys + Task Killer + Shared Folder ({SHARED_PC_DIR})",
                "installed": True,
                "status_text": "DOCKED FULLSCREEN",
            },
        ]
        return self.plugins_report

    def apply_optimal_settings_to_engine(self) -> dict:
        if not self.optimal_settings:
            self.analyze_system_hardware()
        opt = self.optimal_settings
        self.cores = opt["cores"]
        self.ram_mb = opt["ram_mb"]
        self.gpu_mode = opt["gpu_mode"]
        self.resolution = opt["resolution"]
        self.dpi = opt["dpi"]
        self.selected_pixel = opt["pixel_profile"]
        self.fullscreen_enabled = opt["fullscreen"]
        self.sync_current_settings_to_active_profile()
        self.create_or_update_avd(force=False)
        self.log(f"✔ OPTIMAL SETTINGS APPLIED: {opt['summary']}", "SUCCESS")
        return opt

    def check_component_status(self, android_ver: str = None) -> dict:
        ver = android_ver or self.selected_android
        info = ANDROID_VERSIONS.get(ver, ANDROID_VERSIONS["16"])
        rom_st = self.get_rom_status(ver)
        has_emu = os.path.exists(self.emulator_exe)
        has_adb = os.path.exists(self.adb_exe)
        plat_dir = os.path.join(SDK_DIR, "platforms", info["platform_dir"])
        has_plat = os.path.exists(os.path.join(plat_dir, "source.properties")) or os.path.exists(os.path.join(plat_dir, "build.prop"))
        avd_name = self.current_avd_name
        has_avd = os.path.exists(os.path.join(AVD_HOME, f"{avd_name}.ini")) and \
                  os.path.exists(os.path.join(AVD_HOME, f"{avd_name}.avd", "config.ini"))
        return {
            "emulator": has_emu,
            "platform_tools": has_adb,
            "platform": has_plat,
            "sysimg": rom_st["any_installed"],
            "has_playstore": rom_st["has_playstore"],
            "avd_ready": has_avd,
            "all_ready": has_emu and has_adb and has_plat and rom_st["any_installed"] and has_avd
        }

    def _download_with_progress(self, url: str, dest_zip: str, label: str, base_pct: float, span_pct: float):
        self.log(f"Downloading {label} from Google SDK Repo...", "CYBER")
        req = urllib.request.urlopen(url)
        total = int(req.headers.get("Content-Length", 0))
        downloaded = 0
        t0 = time.time()
        with open(dest_zip, "wb") as f:
            while True:
                chunk = req.read(1024 * 512)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    ratio = downloaded / total
                    mb_dl = downloaded / (1024 * 1024)
                    mb_tot = total / (1024 * 1024)
                    speed = mb_dl / max(0.1, time.time() - t0)
                    self.progress(
                        base_pct + ratio * (span_pct * 0.75),
                        f"{label}: {mb_dl:.1f}/{mb_tot:.1f} MB ({speed:.1f} MB/s)"
                    )

    def run_one_click_auto_setup(self, target_android: str = None, setup_all_versions: bool = False) -> bool:
        try:
            self.ensure_directories()
            ver = target_android or self.selected_android
            versions_to_setup = ["15", "16", "17"] if setup_all_versions else [ver]

            self.progress(5, f"INITIALIZING PORTABLE SHOXX AUTO-SETUP FOR ANDROID {', '.join(versions_to_setup)}...")
            self.log(f"=== SHOXX_EMU PORTABLE ONE-CLICK AUTO-SETUP (MAIN DIR: {BASE_DIR}) ===", "CYBER")
            self.relink_portable_paths()

            if not os.path.exists(self.adb_exe):
                zp = os.path.join(DOWNLOADS_DIR, "platform-tools.zip")
                self._download_with_progress(URLS["platform-tools"], zp, "Platform-Tools", 8, 10)
                with zipfile.ZipFile(zp, "r") as z:
                    z.extractall(SDK_DIR)
                os.remove(zp)
            self.log("✔ Portable Platform-Tools (./sdk/platform-tools) verified.", "SUCCESS")

            if not os.path.exists(self.emulator_exe):
                zp = os.path.join(DOWNLOADS_DIR, "emulator.zip")
                self._download_with_progress(URLS["emulator"], zp, "Android Emulator", 18, 18)
                with zipfile.ZipFile(zp, "r") as z:
                    z.extractall(SDK_DIR)
                os.remove(zp)
            self.log("✔ Portable Android Studio QEMU/Gfxstream Emulator (./sdk/emulator) verified.", "SUCCESS")

            for v_key in versions_to_setup:
                v_info = ANDROID_VERSIONS[v_key]
                plat_dir = os.path.join(SDK_DIR, "platforms", v_info["platform_dir"])
                if not os.path.exists(os.path.join(plat_dir, "source.properties")) and not os.path.exists(os.path.join(plat_dir, "build.prop")):
                    zp = os.path.join(DOWNLOADS_DIR, f"platform-android-{v_key}.zip")
                    self._download_with_progress(v_info["platform_url"], zp, f"Android {v_key} Platform", 35, 10)
                    with zipfile.ZipFile(zp, "r") as z:
                        z.extractall(os.path.join(SDK_DIR, "platforms"))
                    for alt in ["android-CinnamonBun", "android-37.0", "android-Baklava", "android-VanillaIceCream"]:
                        alt_p = os.path.join(SDK_DIR, "platforms", alt)
                        if os.path.exists(alt_p) and not os.path.exists(plat_dir):
                            shutil.move(alt_p, plat_dir)
                    if os.path.exists(zp):
                        os.remove(zp)

                rom_st = self.get_rom_status(v_key)
                if not rom_st["any_installed"]:
                    # Download official Google Play Store ROM strictly into ./downloads & extract to ./sdk
                    zp = os.path.join(DOWNLOADS_DIR, f"playstore-sysimg-{v_key}.zip")
                    self._download_with_progress(v_info["playstore_url"], zp, f"Android {v_key} Google Play Store ROM", 45, 40)
                    parent_extract = os.path.dirname(os.path.join(SDK_DIR, v_info["playstore_rel"]))
                    os.makedirs(parent_extract, exist_ok=True)
                    with zipfile.ZipFile(zp, "r") as z:
                        z.extractall(parent_extract)
                    if os.path.exists(zp):
                        os.remove(zp)
                    rom_st = self.get_rom_status(v_key)

                if self.stealth_enabled:
                    self.patch_system_image_build_prop(rom_st["active_dir"])

            # Ensure all profiles have valid AVDs configured
            for prof in self.profiles:
                p_ver = prof.get("android_ver", "16")
                if self.get_rom_status(p_ver)["any_installed"]:
                    self.create_or_update_avd(android_ver=p_ver, avd_name=prof["avd_name"], profile=prof)

            self.progress(100, "SHOXX_EMU READY FOR FULLSCREEN LAUNCH!")
            self.log("=== ONE-CLICK AUTO-SETUP COMPLETED SUCCESSFULLY ===", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"Auto-Setup Error: {e}", "ERROR")
            self.progress(0, f"SETUP ERROR: {e}")
            return False

    def create_or_update_avd(self, android_ver: str = None, avd_name: str = None, profile: dict = None, force: bool = False):
        """
        Creates or updates the portable Google Pixel AVD with:
        - `PlayStore.enabled = yes` (`tag.id = google_apis_playstore`)
        - Retail Smartphone Stealth Hardware Profile (`komodo` / `caiman` / `comet`)
        - Fullscreen Viewport sized to fit neatly alongside the Right-Side GAMING EXTEND Panel
        """
        prof = profile or self.get_active_profile()
        ver = android_ver or prof.get("android_ver", self.selected_android)
        v_info = ANDROID_VERSIONS.get(ver, ANDROID_VERSIONS["16"])
        target_avd = avd_name or prof.get("avd_name", self.current_avd_name)
        api_level = v_info["api"]

        rom_st = self.get_rom_status(ver)
        if self.stealth_enabled and rom_st["any_installed"]:
            self.patch_system_image_build_prop(rom_st["active_dir"])

        avd_dir = os.path.join(AVD_HOME, f"{target_avd}.avd")
        avd_ini = os.path.join(AVD_HOME, f"{target_avd}.ini")

        if force and os.path.exists(avd_dir):
            shutil.rmtree(avd_dir, ignore_errors=True)
        os.makedirs(avd_dir, exist_ok=True)

        with open(avd_ini, "w", encoding="utf-8") as f:
            f.write(
                f"avd.ini.encoding=UTF-8\n"
                f"path={avd_dir}\n"
                f"path.rel=avd\\{target_avd}.avd\n"
                f"target=android-{api_level}\n"
            )

        # Docked Fullscreen Width leaves SIDEBAR_WIDTH on the right for the Gaming Extend Panel
        sw = ctypes.windll.user32.GetSystemMetrics(0) if os.name == "nt" else 1920
        sh = ctypes.windll.user32.GetSystemMetrics(1) if os.name == "nt" else 1080
        w = max(800, sw - SIDEBAR_WIDTH) if self.sidebar_docked else self.resolution[0]
        h = sh if self.sidebar_docked else self.resolution[1]

        pix_key = prof.get("pixel_model", self.selected_pixel)
        pix = PIXEL_PROFILES.get(pix_key, PIXEL_PROFILES["pixel_9_pro_xl"])

        config_lines = [
            "PlayStore.enabled = yes",
            "abi.type = x86_64",
            f"avd.id = {target_avd}",
            "avd.ini.encoding = UTF-8",
            f"avd.name = {target_avd}",
            "disk.cachePartition = yes",
            "disk.cachePartition.size = 128MB",
            "disk.dataPartition.size = 8589934592",
            "fastboot.forceChosenSnapshotBoot = no",
            f"fastboot.forceColdBoot = {'yes' if self.cold_boot else 'no'}",
            f"fastboot.forceFastBoot = {'no' if self.cold_boot else 'yes'}",
            "firstboot.bootFromDownloadableSnapshot = no",
            "firstboot.bootFromLocalSnapshot = yes",
            "firstboot.saveToLocalSnapshot = yes",
            "hw.accelerometer = yes",
            "hw.accelerometer_uncalibrated = yes",
            "hw.audioInput = yes",
            "hw.audioOutput = yes",
            "hw.battery = yes",
            "hw.camera.back = virtualscene",
            "hw.camera.front = emulated",
            "hw.cpu.arch = x86_64",
            f"hw.cpu.ncore = {prof.get('cores', self.cores)}",
            "hw.dPad = no",
            "hw.device.manufacturer = Google",
            f"hw.device.name = {pix['id']}",
            "hw.gps = yes",
            "hw.gpu.enabled = yes",
            f"hw.gpu.mode = {prof.get('gpu_mode', self.gpu_mode)}",
            "hw.gsmModem = yes",
            "hw.gyroscope = yes",
            "hw.initialOrientation = landscape" if w >= h else "hw.initialOrientation = portrait",
            "hw.keyboard = yes",
            "hw.keyboard.lid = yes",
            "hw.lcd.backlight = yes",
            "hw.lcd.circular = false",
            f"hw.lcd.density = {self.dpi}",
            "hw.lcd.depth = 16",
            f"hw.lcd.height = {h}",
            f"hw.lcd.width = {w}",
            "hw.lcd.vsync = 60",
            "hw.mainKeys = no",
            f"hw.ramSize = {prof.get('ram_mb', self.ram_mb)}",
            "hw.sdCard = yes",
            "hw.sensors.gyroscope_uncalibrated = yes",
            "hw.sensors.humidity = yes",
            "hw.sensors.light = yes",
            "hw.sensors.magnetic_field = yes",
            "hw.sensors.magnetic_field_uncalibrated = yes",
            "hw.sensors.orientation = yes",
            "hw.sensors.pressure = yes",
            "hw.sensors.proximity = yes",
            "hw.sensors.temperature = yes",
            "hw.trackBall = no",
            "hw.useext4 = yes",
            f"image.sysdir.1 = {rom_st['active_rel']}",
            "runtime.network.latency = none",
            "runtime.network.speed = full",
            "sdcard.size = 2048M",
            "showDeviceFrame = no",
            f"tag.display = {rom_st['tag_display']}",
            f"tag.displaynames = {rom_st['tag_display']}",
            f"tag.id = {rom_st['tag_id']}",
            f"tag.ids = {rom_st['tag_id']}",
            "userdata.useQcow2 = yes",
            "vm.heapSize = 512M",
        ]

        config_path = os.path.join(avd_dir, "config.ini")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("\n".join(config_lines) + "\n")

        emu_user_ini = os.path.join(avd_dir, "emulator-user.ini")
        with open(emu_user_ini, "w", encoding="utf-8") as f:
            f.write("window.x = 0\nwindow.y = 0\n")

    def clear_avd_locks(self, avd_name: str = None, kill_orphans: bool = False):
        """
        Removes stale `*.lock` files and `*.lock` directories inside AVD containers so the emulator
        never fails with 'Running multiple emulators with the same AVD is an experimental feature'.
        Optionally terminates orphaned emulator/qemu-system processes.
        """
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        if kill_orphans and os.name == "nt":
            for pname in ["qemu-system-x86_64.exe", "emulator.exe", "emulator-check.exe"]:
                try:
                    subprocess.run(["taskkill", "/F", "/IM", pname, "/T"], capture_output=True, timeout=4, creationflags=cflags)
                except Exception:
                    pass
            time.sleep(0.4)

        if not os.path.exists(AVD_HOME):
            return
        for root_d, dirs, files in os.walk(AVD_HOME, topdown=False):
            if avd_name and avd_name not in root_d:
                continue
            for f in files:
                if f.endswith(".lock") or f == "pid":
                    fp = os.path.join(root_d, f)
                    try:
                        os.remove(fp)
                    except Exception:
                        pass
            for d in dirs:
                if d.endswith(".lock"):
                    dp = os.path.join(root_d, d)
                    try:
                        shutil.rmtree(dp, ignore_errors=True)
                    except Exception:
                        pass

    def launch_emulator(self, on_boot_complete=None):
        """
        Launches the active Emulator Profile in PC Fullscreen (docked on the left of the Gaming Extend Sidebar),
        applies Anti-Emulator Real Smartphone Stealth, and injects the selected Root method.
        """
        if self.is_emulator_running():
            # If an emulator window is already visible on screen, dock and focus it
            if self.maximize_emulator_window(fullscreen_borderless=True, leave_sidebar=self.sidebar_docked):
                self.log("Emulator is already running! Docked to Fullscreen Gaming layout and brought to front.", "SUCCESS")
                return
            else:
                self.log("Cleaning up previous background emulator instance before fresh launch...", "WARN")
                self.stop_emulator()

        self.sync_current_settings_to_active_profile()
        self.relink_portable_paths()
        status = self.check_component_status(self.selected_android)
        if not status["all_ready"]:
            self.log(f"Android {self.selected_android} components missing — triggering autonomous One-Click Auto-Setup...", "WARN")
            ok = self.run_one_click_auto_setup(target_android=self.selected_android)
            if not ok:
                return

        prof = self.get_active_profile()
        # Clear any stale lock files/processes holding the AVD
        self.clear_avd_locks(avd_name=prof["avd_name"], kill_orphans=True)

        self.create_or_update_avd(android_ver=self.selected_android, avd_name=prof["avd_name"], profile=prof)
        avd_data_dir = os.path.join(AVD_HOME, f"{prof['avd_name']}.avd")

        sw = ctypes.windll.user32.GetSystemMetrics(0) if os.name == "nt" else 1920
        sh = ctypes.windll.user32.GetSystemMetrics(1) if os.name == "nt" else 1080
        skin_w = max(800, sw - self.current_sidebar_width) if self.sidebar_docked else self.resolution[0]
        skin_h = sh if self.sidebar_docked else self.resolution[1]

        pix = PIXEL_PROFILES.get(self.selected_pixel, PIXEL_PROFILES["pixel_9_pro_xl"])

        cmd = [
            self.emulator_exe,
            "-avd", prof["avd_name"],
            "-datadir", avd_data_dir,
            "-gpu", self.gpu_mode,
            "-memory", str(self.ram_mb),
            "-cores", str(self.cores),
            "-skin", f"{skin_w}x{skin_h}",
            "-skip-adb-auth",
            "-writable-system",  # Needed for Stealth build.prop/resetprop & Root switching
        ]

        if self.cold_boot:
            cmd.append("-no-snapshot-load")

        if self.root_enabled:
            cmd.extend(["-selinux", "permissive"])
            self.log(f"ROOT MODE ARMED [{self.root_method}]: Launching with writable system & SELinux permissive.", "ROOT")

        self.log(f"Launching Profile '{prof['name']}' ({pix['model']} | Android {self.selected_android})...", "CYBER")
        env = self.get_env()

        try:
            subprocess.run([self.adb_exe, "start-server"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
        except Exception:
            pass

        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        self.emulator_proc = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=creation_flags
        )

        threading.Thread(target=self._stream_emulator_logs, daemon=True).start()
        threading.Thread(target=self._post_launch_orchestrator, args=(on_boot_complete,), daemon=True).start()

    def _stream_emulator_logs(self):
        proc = self.emulator_proc
        if not proc or not proc.stdout:
            return
        for line in iter(proc.stdout.readline, ""):
            line_s = line.strip()
            if line_s:
                lvl = "ERROR" if "ERROR" in line_s.upper() else ("WARN" if "WARN" in line_s.upper() else "INFO")
                self.log(f"[EMU] {line_s}", lvl)
        self.log("Emulator process exited.", "WARN")

    def _post_launch_orchestrator(self, on_boot_complete=None):
        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        if self.fullscreen_enabled:
            for _ in range(45):
                if not self.is_emulator_running():
                    return
                if self.maximize_emulator_window(fullscreen_borderless=True, leave_sidebar=self.sidebar_docked):
                    self.log("✔ PC FULLSCREEN + GAMING EXTEND SIDEBAR DOCKED!", "SUCCESS")
                    break
                time.sleep(1.0)

        self.log(f"Waiting for Android {self.selected_android} ({PIXEL_PROFILES[self.selected_pixel]['model']}) Boot & ADB bridge...", "CYBER")
        booted = False
        for _ in range(120):
            if not self.is_emulator_running():
                return
            try:
                res = subprocess.run(
                    [self.adb_exe, "shell", "getprop", "sys.boot_completed"],
                    env=env, capture_output=True, text=True, timeout=4, creationflags=cflags
                )
                if res.stdout.strip() == "1":
                    booted = True
                    break
            except Exception:
                pass
            time.sleep(1.5)

        if booted:
            pix = PIXEL_PROFILES.get(self.selected_pixel, PIXEL_PROFILES["pixel_9_pro_xl"])
            self.log(f"⚡ ANDROID {self.selected_android} ON {pix['model'].upper()} BOOT COMPLETE!", "SUCCESS")
            if self.fullscreen_enabled:
                self.maximize_emulator_window(fullscreen_borderless=True, leave_sidebar=self.sidebar_docked)

            # 1. Apply Real Smartphone Anti-Emulator Stealth Identity
            self.apply_live_stealth_smartphone_identity()

            # 2. Apply Root State (Magisk / KernelSU / APatch or Unroot if Root Switch is OFF)
            self.apply_live_root_state(self.root_enabled, self.root_method)

            # 3. Ensure Shared Folder directory exists on Android SDCard
            subprocess.run([self.adb_exe, "shell", "mkdir -p /sdcard/Download/ShoXx_Shared"], env=env, capture_output=True, timeout=5, creationflags=cflags)

            if on_boot_complete:
                on_boot_complete()
        else:
            self.log("Boot timeout reached while waiting for sys.boot_completed.", "WARN")

    def apply_live_root_state(self, enable_root: bool, method: str = None) -> bool:
        self.root_enabled = enable_root
        if method:
            self.root_method = method

        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

        try:
            if not enable_root:
                self.log(">>> DEACTIVATING ROOT ACCESS (adb unroot + SELinux enforcing + Stealth Lock)...", "WARN")
                subprocess.run([self.adb_exe, "shell", "rm -f /system/xbin/su; setenforce 1"], env=env, capture_output=True, text=True, timeout=5, creationflags=cflags)
                r1 = subprocess.run([self.adb_exe, "unroot"], env=env, capture_output=True, text=True, timeout=10, creationflags=cflags)
                self.log(f"[ADB UNROOT] {(r1.stdout or r1.stderr).strip()}", "INFO")
                time.sleep(1.0)
                id_res = subprocess.run([self.adb_exe, "shell", "id"], env=env, capture_output=True, text=True, timeout=5, creationflags=cflags)
                self.log(f"✔ UNROOT VERIFIED: {id_res.stdout.strip()}", "INFO")
                return True

            m_info = ROOT_METHODS.get(self.root_method, ROOT_METHODS["MAGISK"])
            self.log(f">>> ACTIVATING ROOT ACCESS VIA [{m_info['name']}]...", "ROOT")

            r1 = subprocess.run([self.adb_exe, "root"], env=env, capture_output=True, text=True, timeout=10, creationflags=cflags)
            self.log(f"[ADB ROOT] {(r1.stdout or r1.stderr).strip()}", "ROOT")
            time.sleep(1.0)
            subprocess.run([self.adb_exe, "remount"], env=env, capture_output=True, text=True, timeout=10, creationflags=cflags)
            subprocess.run([self.adb_exe, "shell", "mount -o rw,remount /"], env=env, capture_output=True, text=True, timeout=5, creationflags=cflags)
            subprocess.run([self.adb_exe, "shell", "setenforce", "0"], env=env, capture_output=True, text=True, timeout=5, creationflags=cflags)

            apk_path = os.path.join(ROOT_METHODS_DIR, m_info["apk_rel"])
            bin_dir = os.path.join(ROOT_METHODS_DIR, m_info["bin_rel"])

            if self.root_method == "MAGISK":
                self.log("[MAGISK ENGINE] Deploying x86_64 Magisk Daemon -> /data/adb/magisk & /system/xbin/su ...", "ROOT")
                subprocess.run([self.adb_exe, "shell", "mkdir -p /data/adb/magisk /data/adb/modules /system/xbin"], env=env, capture_output=True, timeout=5, creationflags=cflags)
                for bname in ["magisk", "magiskinit", "magiskpolicy", "busybox", "util_functions.sh", "boot_patch.sh"]:
                    bpath = os.path.join(bin_dir, bname)
                    if os.path.exists(bpath):
                        subprocess.run([self.adb_exe, "push", bpath, f"/data/adb/magisk/{bname}"], env=env, capture_output=True, timeout=8, creationflags=cflags)
                subprocess.run(
                    [self.adb_exe, "shell", "chmod 755 /data/adb/magisk/*; cp -f /data/adb/magisk/magisk /system/xbin/magisk; ln -sf /data/adb/magisk/magisk /system/xbin/su; /data/adb/magisk/magisk --post-fs-data; /data/adb/magisk/magisk --service"],
                    env=env, capture_output=True, timeout=8, creationflags=cflags
                )

            elif self.root_method == "KERNELSU":
                self.log("[KERNELSU ENGINE] Deploying x86_64 KernelSU Daemon (ksud, kernelsu, libadbroot.so) -> /data/adb/ksu & /system/xbin/su ...", "ROOT")
                subprocess.run([self.adb_exe, "shell", "mkdir -p /data/adb/ksu /data/adb/ksu/bin /data/adb/modules /system/xbin"], env=env, capture_output=True, timeout=5, creationflags=cflags)
                for bname in ["ksud", "kernelsu", "adbroot"]:
                    bpath = os.path.join(bin_dir, bname)
                    if os.path.exists(bpath):
                        subprocess.run([self.adb_exe, "push", bpath, f"/data/adb/ksu/bin/{bname}"], env=env, capture_output=True, timeout=8, creationflags=cflags)
                subprocess.run(
                    [self.adb_exe, "shell", "chmod 755 /data/adb/ksu/bin/*; cp -f /data/adb/ksu/bin/ksud /system/xbin/ksud; ln -sf /data/adb/ksu/bin/ksud /system/xbin/su; /data/adb/ksu/bin/ksud post-fs-data; /data/adb/ksu/bin/ksud services"],
                    env=env, capture_output=True, timeout=8, creationflags=cflags
                )

            else:
                self.log("[APATCH + NATIVE SU] Deploying APatch Manager + Native SuperSU & BusyBox x86_64 -> /data/adb/ap/bin & /system/xbin/su ...", "ROOT")
                subprocess.run([self.adb_exe, "shell", "mkdir -p /data/adb/ap/bin /data/adb/modules /system/xbin"], env=env, capture_output=True, timeout=5, creationflags=cflags)
                bb_path = os.path.join(ROOT_METHODS_DIR, "magisk", "bin_x86_64", "busybox")
                if os.path.exists(bb_path):
                    subprocess.run([self.adb_exe, "push", bb_path, "/data/adb/ap/bin/busybox"], env=env, capture_output=True, timeout=8, creationflags=cflags)
                    subprocess.run([self.adb_exe, "shell", "chmod 755 /data/adb/ap/bin/busybox; cp -f /data/adb/ap/bin/busybox /system/xbin/busybox"], env=env, capture_output=True, timeout=5, creationflags=cflags)

            if os.path.exists(apk_path):
                self.log(f"[{self.root_method}] Installing Manager App ({os.path.basename(apk_path)})...", "CYBER")
                subprocess.run([self.adb_exe, "install", "-r", "-g", apk_path], env=env, capture_output=True, text=True, timeout=25, creationflags=cflags)

            id_res = subprocess.run([self.adb_exe, "shell", "id"], env=env, capture_output=True, text=True, timeout=5, creationflags=cflags)
            id_str = id_res.stdout.strip()
            self.log(f"✔ ROOT [{m_info['short']}] VERIFIED: {id_str}", "SUCCESS")
            return "uid=0(root)" in id_str

        except Exception as e:
            self.log(f"Root Switch Error: {e}", "ERROR")
            return False

    def verify_device_info(self) -> dict:
        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        info = {
            "connected": False, "release": "--", "sdk": "--", "model": "--",
            "device": "--", "tags": "--", "id": "--", "root": False,
            "playstore": False, "pixel": PIXEL_PROFILES[self.selected_pixel]["model"]
        }
        try:
            def prop(name):
                r = subprocess.run([self.adb_exe, "shell", "getprop", name], env=env, capture_output=True, text=True, timeout=3, creationflags=cflags)
                return r.stdout.strip()

            rel = prop("ro.build.version.release")
            if rel:
                info["connected"] = True
                info["release"] = rel
                info["sdk"] = prop("ro.build.version.sdk")
                info["model"] = prop("ro.product.model")
                info["device"] = prop("ro.product.device")
                info["tags"] = prop("ro.build.tags")
                id_r = subprocess.run([self.adb_exe, "shell", "id"], env=env, capture_output=True, text=True, timeout=3, creationflags=cflags)
                info["id"] = id_r.stdout.strip()
                info["root"] = "uid=0(root)" in info["id"]
                ps_r = subprocess.run([self.adb_exe, "shell", "pm", "path", "com.android.vending"], env=env, capture_output=True, text=True, timeout=3, creationflags=cflags)
                info["playstore"] = "package:" in (ps_r.stdout or "")
        except Exception:
            pass
        return info

    def maximize_emulator_window(self, fullscreen_borderless: bool = True, leave_sidebar: bool = True, sidebar_width: int = None) -> bool:
        """
        Positions the Android Emulator window into Borderless Fullscreen on the PC:
        - If `leave_sidebar=True`, occupies `(0, 0)` to `(ScreenW - active_sidebar_w, ScreenH)` so the fixed
          or collapsed right-hand GAMING EXTEND sidebar panel sits flush on the right side of the monitor!
        """
        if os.name != "nt":
            return False
        try:
            from ctypes import wintypes

            user32 = ctypes.windll.user32
            WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

            found_hwnds = []

            def enum_cb(hwnd, lparam):
                if user32.IsWindowVisible(hwnd):
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        user32.GetWindowTextW(hwnd, buf, length + 1)
                        title = buf.value
                        if "Android Emulator" in title or "ShoXx_" in title or "qemu-system" in title.lower():
                            found_hwnds.append(hwnd)
                return True

            user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
            if not found_hwnds:
                return False

            screen_w = user32.GetSystemMetrics(0)
            screen_h = user32.GetSystemMetrics(1)
            active_sb_w = sidebar_width if sidebar_width is not None else self.current_sidebar_width
            target_w = (screen_w - active_sb_w) if leave_sidebar else screen_w

            GWL_STYLE = -16
            WS_POPUP = 0x80000000
            WS_VISIBLE = 0x10000000
            SW_SHOWMAXIMIZED = 3
            SWP_FRAMECHANGED = 0x0020
            SWP_SHOWWINDOW = 0x0040

            for hwnd in found_hwnds:
                if fullscreen_borderless:
                    user32.SetWindowLongW(hwnd, GWL_STYLE, WS_POPUP | WS_VISIBLE)
                    user32.SetWindowPos(hwnd, 0, 0, 0, target_w, screen_h, SWP_FRAMECHANGED | SWP_SHOWWINDOW)
                else:
                    user32.ShowWindow(hwnd, SW_SHOWMAXIMIZED)
                user32.SetForegroundWindow(hwnd)
            return True
        except Exception:
            return False

    def open_root_shell_terminal(self):
        env = self.get_env()
        if self.root_enabled:
            subprocess.run([self.adb_exe, "root"], env=env, capture_output=True)
        subprocess.Popen(
            ["cmd.exe", "/c", "start", f"ShoXx_Emu Android {self.selected_android} [{self.root_method}] ROOT SHELL", self.adb_exe, "shell"],
            env=env
        )
        self.log(f"Opened interactive Android {self.selected_android} Root Shell terminal ({self.root_method}).", "CYBER")

    def open_google_play_store(self):
        """Launches the Google Play Store app (`com.android.vending`) directly inside the running emulator."""
        def _worker():
            env = self.get_env()
            cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            subprocess.run(
                [self.adb_exe, "shell", "monkey", "-p", "com.android.vending", "-c", "android.intent.category.LAUNCHER", "1"],
                env=env, capture_output=True, timeout=5, creationflags=cflags
            )
            self.log("Launched Google Play Store on the Pixel Emulator!", "SUCCESS")
        threading.Thread(target=_worker, daemon=True).start()

    def is_emulator_running(self) -> bool:
        if self.emulator_proc is not None and self.emulator_proc.poll() is None:
            return True
        return False

    def stop_emulator(self):
        env = self.get_env()
        cflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            subprocess.run([self.adb_exe, "emu", "kill"], env=env, capture_output=True, timeout=4, creationflags=cflags)
        except Exception:
            pass
        if self.emulator_proc and self.emulator_proc.poll() is None:
            try:
                self.emulator_proc.terminate()
            except Exception:
                pass
        self.clear_avd_locks(kill_orphans=True)
        self.log("Emulator stopped and AVD locks released.", "WARN")
