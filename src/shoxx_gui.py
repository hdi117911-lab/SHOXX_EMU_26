# -*- coding: utf-8 -*-
"""
ShoXx_Emu - Enterprise Studio Edition (Clean, Elegant, Professional Dark UI)
Features:
- Refined Obsidian / Slate Dark Theme with crisp Cobalt Accent & Subtle Emerald Status Indicators
- Clean, Animated Executive Boot & System Diagnostics Splash Overlay
- Multi-Profile Manager Submenu (Create, Switch, Delete Profiles with Unique Stealth IMEI/Serial)
- Fixed Right-Side "GAMING EXTEND" Dock Panel (320px, cleanly organized for Fullscreen Operation):
  * Android Navigation Bar: Back, Home, Recents + Running Background Apps Task Manager
  * APK & XAPK Bundle Installer (with File Dialog)
  * Shared PC <-> Emulator Folder Sync Bridge
  * Stealth Identity & Fullscreen Docking Controls
- Android 15 / 16 / 17 Selector (with Google Play Store ROM Manager & In-App Downloader)
- Switchable 3-Method Root Engine (1. Magisk, 2. KernelSU, 3. APatch + Native SU)
"""

import os
import sys
import math
import time
import ctypes
import zipfile
import threading
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageEnhance

from shoxx_engine import (
    ShoXxEngine,
    ANDROID_VERSIONS,
    PIXEL_PROFILES,
    ROOT_METHODS,
    SIDEBAR_WIDTH,
    SIDEBAR_COLLAPSED_WIDTH,
    BASE_DIR,
    SDK_DIR,
    AVD_HOME,
    SHARED_PC_DIR,
    generate_random_imei,
)

# =============================================================================
# PROFESSIONAL STUDIO DARK PALETTE (CLEAN, ELEGANT, HIGH-CONTRAST)
# =============================================================================
BG_ROOT = "#0B0E14"         # Deep Obsidian Background
BG_SURFACE = "#111621"      # Primary Panel Surface
BG_CARD = "#161D2B"         # Elevated Card Background
BG_INPUT = "#0E131D"        # Subtle Input/List Background
BG_SIDEBAR = "#0E121B"      # Right Docked Gaming Extend Sidebar
BORDER_SUBTLE = "#222C3F"   # Crisp 1px Structural Hairline Border
BORDER_FOCUS = "#3B82F6"    # Active Selection Border

ACCENT_PRIMARY = "#3B82F6"  # Executive Cobalt Blue
ACCENT_HOVER = "#2563EB"    # Deeper Cobalt Hover
STATUS_OK = "#10B981"       # Emerald Green
STATUS_WARN = "#F59E0B"     # Warm Amber
STATUS_ERR = "#EF4444"      # Clean Crimson

TEXT_PRIMARY = "#F1F5F9"    # Crisp Slate White
TEXT_SECONDARY = "#94A3B8"  # Muted Steel Gray
TEXT_MUTED = "#64748B"      # Subtle Caption Gray

FONT_UI = "Segoe UI"
FONT_MONO = "Consolas"


class ExecutiveSplashOverlay(tk.Frame):
    """
    4-Second Animated Boot Splash Screen featuring `D:\\SHOXX_EMU_26\\splash.jpg`
    with a subtle, realistic flickering neon light effect + live hardware telemetry bar.
    """

    def __init__(self, parent, engine: ShoXxEngine, on_complete):
        super().__init__(parent, bg=BG_ROOT)
        self.parent = parent
        self.engine = engine
        self.on_complete = on_complete
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.sw = parent.winfo_screenwidth()
        self.sh = parent.winfo_screenheight()

        self.canvas = tk.Canvas(self, width=self.sw, height=self.sh, bg="#06080D", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.sys_rep = self.engine.analyze_system_hardware()
        self.plugins_rep = self.engine.inspect_plugins_and_tools()

        # Pre-generate subtle neon flicker frames from D:\SHOXX_EMU_26\splash.jpg
        self.splash_frames = []
        self.img_w = min(1060, int(self.sw * 0.78))
        self.img_h = min(540, int(self.sh * 0.66))
        self._prepare_neon_splash_frames()

        self.duration_sec = 4.0
        self.start_time = time.time()
        self.frame_idx = 0
        self.running = True
        self._animate()

    def _prepare_neon_splash_frames(self):
        splash_path = os.path.join(BASE_DIR, "splash.jpg")
        if not os.path.isfile(splash_path):
            splash_path = os.path.join(BASE_DIR, "assets", "splash_graffiti.png")
        if not os.path.isfile(splash_path):
            return
        try:
            raw_img = Image.open(splash_path).convert("RGB")
            # Preserve aspect ratio within max splash box
            iw, ih = raw_img.size
            scale = min(self.img_w / max(1, iw), self.img_h / max(1, ih))
            target_w = max(320, int(iw * scale))
            target_h = max(200, int(ih * scale))
            self.img_w, self.img_h = target_w, target_h
            base_img = raw_img.resize((target_w, target_h), Image.Resampling.LANCZOS)

            # 7 subtle brightness + neon color intensity levels for smooth 30+ FPS neon flicker
            levels = [
                (0.84, 0.90),  # 0: Dim flicker dip
                (0.91, 0.95),  # 1: Soft low glow
                (0.96, 0.98),  # 2: Slight warm-up
                (1.00, 1.00),  # 3: Nominal studio neon
                (1.05, 1.08),  # 4: Bright neon pulse
                (1.11, 1.15),  # 5: High neon surge
                (1.17, 1.22),  # 6: Peak neon tube flash
            ]
            for b_fac, c_fac in levels:
                frame = ImageEnhance.Brightness(base_img).enhance(b_fac)
                frame = ImageEnhance.Color(frame).enhance(c_fac)
                self.splash_frames.append(ImageTk.PhotoImage(frame))
        except Exception:
            self.splash_frames = []

    def _compute_neon_flicker(self, elapsed: float):
        """
        Computes a subtle, realistic neon tube light flicker factor (0..6 index + border colors).
        Combines a smooth sine breathing wave with brief, authentic neon gas micro-flickers.
        """
        # Smooth breathing base wave
        wave = 0.5 + 0.5 * math.sin(elapsed * 5.2)

        # Deterministic + subtle stochastic neon tube micro-flickers at characteristic intervals
        micro_dip = 0.0
        for pulse_t in (0.35, 0.42, 1.15, 1.85, 1.92, 2.65, 3.30, 3.38):
            if abs(elapsed - pulse_t) < 0.045:
                micro_dip = -0.38
                break
        for surge_t in (0.75, 1.45, 2.25, 3.05, 3.65):
            if abs(elapsed - surge_t) < 0.055:
                micro_dip = 0.32
                break

        jitter = random.uniform(-0.06, 0.06)
        intensity = max(0.0, min(1.0, wave * 0.65 + 0.25 + micro_dip + jitter))

        if not self.splash_frames:
            return None, "#00F0FF", "#3B82F6", 2

        idx = int(round(intensity * (len(self.splash_frames) - 1)))
        idx = max(0, min(len(self.splash_frames) - 1, idx))

        # Neon border colors synchronized with flicker intensity
        if idx <= 1:
            outer_glow = "#1E3A5F"
            inner_neon = "#0284C7"
            glow_w = 1
        elif idx <= 3:
            outer_glow = "#1D4ED8"
            inner_neon = "#00D8FF"
            glow_w = 2
        elif idx <= 5:
            outer_glow = "#3B82F6"
            inner_neon = "#38BDF8"
            glow_w = 3
        else:
            outer_glow = "#A855F7"
            inner_neon = "#67E8F9"
            glow_w = 4

        return self.splash_frames[idx], outer_glow, inner_neon, glow_w

    def _animate(self):
        if not self.running:
            return

        elapsed = time.time() - self.start_time
        pct = min(100.0, (elapsed / self.duration_sec) * 100.0)

        c = self.canvas
        c.delete("all")
        cx = self.sw // 2
        cy = self.sh // 2

        # Outer Splash Container Size
        hud_h = 112
        pad = 24
        box_w = self.img_w + pad * 2
        box_h = self.img_h + hud_h + pad * 2
        bx1 = cx - box_w // 2
        by1 = cy - box_h // 2
        bx2 = bx1 + box_w
        by2 = by1 + box_h

        frame_photo, outer_glow, inner_neon, glow_w = self._compute_neon_flicker(elapsed)

        # Subtle Ambient Neon Halo behind the Splash Card
        c.create_rectangle(
            bx1 - 6, by1 - 6, bx2 + 6, by2 + 6,
            fill="", outline=outer_glow, width=max(1, glow_w - 1)
        )
        c.create_rectangle(
            bx1 - 2, by1 - 2, bx2 + 2, by2 + 2,
            fill=BG_SURFACE, outline=inner_neon, width=glow_w
        )

        # Render splash.jpg with subtle flickering neon effect
        img_x = cx
        img_y = by1 + pad + self.img_h // 2
        ix1 = cx - self.img_w // 2
        iy1 = by1 + pad
        ix2 = ix1 + self.img_w
        iy2 = iy1 + self.img_h

        if frame_photo is not None:
            c.create_image(img_x, img_y, image=frame_photo, anchor="center")
            # Flickering Neon Frame around splash.jpg
            c.create_rectangle(ix1 - 2, iy1 - 2, ix2 + 2, iy2 + 2, outline=outer_glow, width=glow_w + 1)
            c.create_rectangle(ix1, iy1, ix2, iy2, outline=inner_neon, width=max(1, glow_w - 1))

            # Subtle Corner Neon Tubes
            clen = 28
            for (cx_p, cy_p, dx, dy) in [
                (ix1 - 4, iy1 - 4, 1, 1),
                (ix2 + 4, iy1 - 4, -1, 1),
                (ix1 - 4, iy2 + 4, 1, -1),
                (ix2 + 4, iy2 + 4, -1, -1),
            ]:
                c.create_line(cx_p, cy_p, cx_p + dx * clen, cy_p, fill=inner_neon, width=2)
                c.create_line(cx_p, cy_p, cx_p, cy_p + dy * clen, fill=inner_neon, width=2)

        # Bottom Executive Telemetry & Progress HUD Strip
        hy1 = iy2 + 14
        hy2 = by2 - 14
        c.create_rectangle(ix1, hy1, ix2, hy2, fill=BG_CARD, outline=BORDER_SUBTLE, width=1)

        sr = self.sys_rep
        opt = sr["optimal"]
        ready_cnt = sum(1 for p in self.plugins_rep if p["installed"])

        c.create_text(
            ix1 + 16, hy1 + 18,
            text="ShoXx_Emu-26  •  PORTABLE ANDROID 15 / 16 / 17 WORKSTATION",
            font=(FONT_UI, 10, "bold"), fill=inner_neon, anchor="w"
        )
        c.create_text(
            ix2 - 16, hy1 + 18,
            text=f"[ ESC or Click to Skip  •  {max(0.0, self.duration_sec - elapsed):.1f}s ]",
            font=(FONT_MONO, 8), fill=TEXT_MUTED, anchor="e"
        )

        c.create_text(
            ix1 + 16, hy1 + 38,
            text=(
                f"Hardware: {sr['cpu_name']}  |  {sr['ram_total_mb']} MB RAM  |  "
                f"{sr['primary_gpu']['name']}  |  Modules Ready: {ready_cnt}/{len(self.plugins_rep)}  |  "
                f"Optimal: {opt['cores_label']}, {opt['ram_label']}"
            ),
            font=(FONT_UI, 8), fill=TEXT_SECONDARY, anchor="w"
        )

        # Flickering Neon Progress Bar (0 -> 100% over 4.0 seconds)
        p_y1 = hy2 - 22
        p_y2 = hy2 - 12
        p_w = self.img_w - 32
        c.create_rectangle(ix1 + 16, p_y1, ix2 - 16, p_y2, fill=BG_INPUT, outline=BORDER_SUBTLE, width=1)
        fill_w = int(p_w * (pct / 100.0))
        if fill_w > 0:
            c.create_rectangle(ix1 + 16, p_y1, ix1 + 16 + fill_w, p_y2, fill=inner_neon, outline=outer_glow)

        c.bind("<Button-1>", lambda e: self.finish())

        if elapsed >= self.duration_sec:
            self.finish()
        else:
            self.after(30, self._animate)

    def finish(self):
        if not self.running:
            return
        self.running = False
        self.destroy()
        if self.on_complete:
            self.on_complete()


class ProfileManagerModal(tk.Toplevel):
    """
    Clean, Executive Modal Dialog for Managing Multiple Emulator Profiles & Play Store ROMs.
    """

    def __init__(self, parent, engine: ShoXxEngine, on_profile_selected):
        super().__init__(parent)
        self.parent = parent
        self.engine = engine
        self.on_profile_selected = on_profile_selected

        self.title("ShoXx_Emu — Profile & ROM Manager")
        self.configure(bg=BG_SURFACE, highlightbackground=BORDER_SUBTLE, highlightthickness=1)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"900x610+{(sw - 900) // 2}+{(sh - 610) // 2}")
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG_ROOT, pady=14, padx=20)
        hdr.pack(fill="x")
        tk.Label(
            hdr, text="Emulator Profile & ROM Manager",
            font=(FONT_UI, 13, "bold"), fg=TEXT_PRIMARY, bg=BG_ROOT
        ).pack(side="left")
        tk.Button(
            hdr, text="Close", command=self.destroy,
            font=(FONT_UI, 9, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY,
            activebackground=STATUS_ERR, activeforeground=TEXT_PRIMARY,
            relief="flat", padx=14, pady=4, cursor="hand2"
        ).pack(side="right")

        tk.Frame(self, bg=BORDER_SUBTLE, height=1).pack(fill="x")

        body = tk.Frame(self, bg=BG_SURFACE, padx=20, pady=16)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=5)
        body.grid_columnconfigure(1, weight=4)
        body.grid_rowconfigure(0, weight=1)

        # Left: Profiles List
        left_f = tk.Frame(body, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=14, pady=14)
        left_f.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        tk.Label(left_f, text="AVAILABLE PROFILES", font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w", pady=(0, 8))

        self.prof_listbox = tk.Listbox(
            left_f, bg=BG_INPUT, fg=TEXT_PRIMARY,
            selectbackground=ACCENT_PRIMARY, selectforeground=TEXT_PRIMARY,
            font=(FONT_UI, 10), height=10, relief="flat",
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, activestyle="none"
        )
        self.prof_listbox.pack(fill="both", expand=True, pady=4)
        self.prof_listbox.bind("<<ListboxSelect>>", self._on_list_select)

        self.prof_detail_lbl = tk.Label(
            left_f, text="", font=(FONT_MONO, 8), fg=TEXT_SECONDARY,
            bg=BG_INPUT, justify="left", anchor="w", padx=10, pady=8
        )
        self.prof_detail_lbl.pack(fill="x", pady=8)

        act_row = tk.Frame(left_f, bg=BG_CARD)
        act_row.pack(fill="x", pady=(4, 0))
        tk.Button(
            act_row, text="Activate Profile", command=self._activate_selected,
            font=(FONT_UI, 9, "bold"), bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY,
            activebackground=ACCENT_HOVER, relief="flat", padx=12, pady=6, cursor="hand2"
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        tk.Button(
            act_row, text="New IMEI", command=self._regenerate_imei,
            font=(FONT_UI, 9), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            relief="flat", padx=10, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            act_row, text="Delete", command=self._delete_selected,
            font=(FONT_UI, 9), bg=BG_SURFACE, fg=STATUS_ERR,
            relief="flat", padx=10, pady=6, cursor="hand2"
        ).pack(side="right")

        # Right: Create Profile Form & Play Store ROM Manager
        right_f = tk.Frame(body, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=16, pady=14)
        right_f.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        tk.Label(right_f, text="CREATE NEW PROFILE", font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w", pady=(0, 8))

        tk.Label(right_f, text="Profile Name", font=(FONT_UI, 9), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w")
        self.new_name_var = tk.StringVar(value="Pixel Tablet Landscape — Work Profile")
        tk.Entry(
            right_f, textvariable=self.new_name_var, font=(FONT_UI, 10),
            bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY,
            relief="flat", highlightthickness=1, highlightbackground=BORDER_SUBTLE
        ).pack(fill="x", pady=(2, 10), ipady=5)

        tk.Label(right_f, text="Android Version (Google Play Store)", font=(FONT_UI, 9), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w")
        self.new_os_var = tk.StringVar(value="16")
        os_m = tk.OptionMenu(right_f, self.new_os_var, "15", "16", "17")
        os_m.config(bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_UI, 9), highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat")
        os_m.pack(fill="x", pady=(2, 10))

        tk.Label(right_f, text="Retail Tablet / Smartphone Model", font=(FONT_UI, 9), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w")
        self.new_pix_var = tk.StringVar(value="pixel_tablet")
        pix_m = tk.OptionMenu(right_f, self.new_pix_var, *PIXEL_PROFILES.keys())
        pix_m.config(bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_UI, 9), highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat")
        pix_m.pack(fill="x", pady=(2, 10))

        tk.Label(right_f, text="Root Architecture", font=(FONT_UI, 9), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w")
        self.new_rm_var = tk.StringVar(value="MAGISK")
        rm_m = tk.OptionMenu(right_f, self.new_rm_var, "MAGISK", "KERNELSU", "APATCH_SU")
        rm_m.config(bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_UI, 9), highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat")
        rm_m.pack(fill="x", pady=(2, 10))

        self.new_root_chk = tk.BooleanVar(value=True)
        tk.Checkbutton(
            right_f, text="Enable Superuser Root Access", variable=self.new_root_chk,
            bg=BG_CARD, fg=TEXT_PRIMARY, selectcolor=BG_INPUT,
            activebackground=BG_CARD, activeforeground=TEXT_PRIMARY, font=(FONT_UI, 9)
        ).pack(anchor="w", pady=4)

        tk.Button(
            right_f, text="Create & Activate Profile", command=self._create_profile,
            font=(FONT_UI, 9, "bold"), bg=STATUS_OK, fg=BG_ROOT,
            relief="flat", pady=7, cursor="hand2"
        ).pack(fill="x", pady=(8, 14))

        # Play Store ROM Download Section
        tk.Frame(right_f, bg=BORDER_SUBTLE, height=1).pack(fill="x", pady=4)
        tk.Label(right_f, text="GOOGLE PLAY STORE ROM PACKAGES", font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD).pack(anchor="w", pady=(6, 4))

        dl_btns = tk.Frame(right_f, bg=BG_CARD)
        dl_btns.pack(fill="x")
        for v_k in ["15", "16", "17"]:
            st = self.engine.get_rom_status(v_k)
            lbl = f"Android {v_k} ✔" if st["has_playstore"] else f"Download A{v_k}"
            col = STATUS_OK if st["has_playstore"] else ACCENT_PRIMARY
            tk.Button(
                dl_btns, text=lbl,
                command=lambda v=v_k: self._download_rom(v),
                font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=col,
                relief="flat", padx=6, pady=5, cursor="hand2"
            ).pack(side="left", expand=True, fill="x", padx=2)

        # Clean & Portable ZIP Import / Export Section
        tk.Frame(right_f, bg=BORDER_SUBTLE, height=1).pack(fill="x", pady=(10, 4))
        tk.Label(
            right_f, text="PORTABLE ZIP IMPORT & EXPORT",
            font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD
        ).pack(anchor="w", pady=(4, 4))

        exp_row1 = tk.Frame(right_f, bg=BG_CARD)
        exp_row1.pack(fill="x", pady=2)
        exp_row1.grid_columnconfigure((0, 1), weight=1, uniform="expb1")
        tk.Button(
            exp_row1, text="Clean Cache & Relink",
            command=self._clean_and_verify,
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=STATUS_OK,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 3))

        tk.Button(
            exp_row1, text="Import Profile (.zip)",
            command=self._import_profile_zip,
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=ACCENT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=1, sticky="ew", padx=(3, 0))

        exp_row2 = tk.Frame(right_f, bg=BG_CARD)
        exp_row2.pack(fill="x", pady=(4, 0))
        exp_row2.grid_columnconfigure((0, 1), weight=1, uniform="expb")

        tk.Button(
            exp_row2, text="Export Profile (.zip)",
            command=lambda: self._export_zip(mode="profile"),
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            relief="flat", pady=6, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 3))

        tk.Button(
            exp_row2, text="Export Portable Core (.zip)",
            command=lambda: self._export_zip(mode="full_core"),
            font=(FONT_UI, 8, "bold"), bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY,
            activebackground=ACCENT_HOVER, relief="flat", pady=6, cursor="hand2"
        ).grid(row=0, column=1, sticky="ew", padx=(3, 0))

    def _refresh_list(self):
        self.prof_listbox.delete(0, "end")
        active_idx = 0
        for idx, p in enumerate(self.engine.profiles):
            mark = "● " if p["id"] == self.engine.active_profile_id else "  "
            r_str = p.get("root_method", "MAGISK") if p.get("root_enabled", True) else "Unrooted"
            self.prof_listbox.insert("end", f"{mark}{p['name']}  (Android {p['android_ver']} • {r_str})")
            if p["id"] == self.engine.active_profile_id:
                active_idx = idx
        self.prof_listbox.selection_set(active_idx)
        self._on_list_select()

    def _on_list_select(self, event=None):
        sel = self.prof_listbox.curselection()
        if not sel:
            return
        p = self.engine.profiles[sel[0]]
        pix = PIXEL_PROFILES.get(p.get("pixel_model", "pixel_9_pro_xl"), PIXEL_PROFILES["pixel_9_pro_xl"])
        rom_st = self.engine.get_rom_status(p.get("android_ver", "16"))
        play_badge = "Google Play Store Installed" if rom_st["has_playstore"] else "Base ROM (Play Store Downloadable)"
        self.prof_detail_lbl.config(
            text=(
                f"Container : {p['avd_name']}\n"
                f"Device    : {pix['manufacturer']} {pix['model']} ({pix['device']} / release-keys)\n"
                f"OS Image  : Android {p['android_ver']} — {play_badge}\n"
                f"IMEI / SN : {p.get('imei', '--')}  •  {p.get('serial', '--')} ({p.get('carrier', 'Telekom.de')})"
            )
        )

    def _activate_selected(self):
        sel = self.prof_listbox.curselection()
        if not sel:
            return
        p = self.engine.profiles[sel[0]]
        self.engine.select_profile(p["id"])
        self._refresh_list()
        if self.on_profile_selected:
            self.on_profile_selected(p)

    def _regenerate_imei(self):
        sel = self.prof_listbox.curselection()
        if not sel:
            return
        p = self.engine.profiles[sel[0]]
        p["imei"] = generate_random_imei()
        self.engine.save_profiles()
        self._on_list_select()
        if self.engine.is_emulator_running():
            threading.Thread(target=self.engine.apply_live_stealth_smartphone_identity, daemon=True).start()

    def _delete_selected(self):
        sel = self.prof_listbox.curselection()
        if not sel:
            return
        p = self.engine.profiles[sel[0]]
        if self.engine.delete_profile(p["id"]):
            self._refresh_list()
            if self.on_profile_selected:
                self.on_profile_selected(self.engine.get_active_profile())

    def _create_profile(self):
        p = self.engine.create_new_profile(
            name=self.new_name_var.get(),
            android_ver=self.new_os_var.get(),
            pixel_model=self.new_pix_var.get(),
            root_enabled=self.new_root_chk.get(),
            root_method=self.new_rm_var.get(),
            ram_mb=self.engine.ram_mb,
            cores=self.engine.cores
        )
        self._refresh_list()
        if self.on_profile_selected:
            self.on_profile_selected(p)

    def _download_rom(self, ver_k: str):
        self.engine.download_playstore_rom(ver_k, on_done=lambda ok: self.after(0, self._refresh_list))
        messagebox.showinfo(
            "Google Play Store ROM Download",
            f"Downloading official Android {ver_k} Google Play Store system image into ./downloads/.\nProgress is shown in the bottom status bar."
        )

    def _clean_and_verify(self):
        res = self.engine.clean_and_verify_portability()
        messagebox.showinfo(
            "Portability Audit & Cleanup Complete",
            f"Removed {res['cleaned_items']} temporary/lock file(s) ({res['freed_mb']} MB freed).\n"
            f"All AVD .ini paths have been dynamically relinked to:\n{BASE_DIR}"
        )

    def _import_profile_zip(self):
        zip_path = filedialog.askopenfilename(
            parent=self,
            title="Select Portable Profile ZIP Archive to Import",
            initialdir=BASE_DIR,
            filetypes=[("ZIP Archive (*.zip)", "*.zip"), ("All Files (*.*)", "*.*")]
        )
        if not zip_path:
            return
        try:
            imp_p = self.engine.import_profile_zip(zip_path)
            self._refresh_list()
            if self.on_profile_selected:
                self.on_profile_selected(imp_p)
            messagebox.showinfo(
                "Portable Profile Imported",
                f"Profile '{imp_p['name']}' ({imp_p['avd_name']}) has been imported,\n"
                f"relinked to {BASE_DIR}, and set as active!"
            )
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import profile ZIP:\n{e}")

    def _export_zip(self, mode: str = "profile"):
        sel = self.prof_listbox.curselection()
        prof = self.engine.profiles[sel[0]] if sel else self.engine.get_active_profile()
        default_name = f"{prof['avd_name']}_Portable_Profile.zip" if mode == "profile" else "ShoXx_Emu_Portable_Core.zip"
        dest_path = filedialog.asksaveasfilename(
            parent=self,
            title="Save Portable ZIP Archive",
            initialdir=BASE_DIR,
            initialfile=default_name,
            defaultextension=".zip",
            filetypes=[("ZIP Archive (*.zip)", "*.zip")]
        )
        if not dest_path:
            return

        def _done_cb(ok, path_or_err, size_mb):
            if ok:
                self.after(0, lambda: messagebox.showinfo(
                    "Portable ZIP Export Complete",
                    f"Archive successfully created:\n{path_or_err}\nSize: {size_mb} MB"
                ))
            else:
                self.after(0, lambda: messagebox.showerror(
                    "Export Error",
                    f"Failed to create ZIP archive:\n{path_or_err}"
                ))

        self.engine.export_portable_zip(dest_path, mode=mode, profile_id=prof["id"], on_done=_done_cb)


class KeymapperStudioModal(tk.Toplevel):
    """
    Interactive Widescreen Keymapping Studio (1580x1080 Landscape Tablet Mode).
    Allows configuring WASD movement + free touch points on a proportional 1580x1080 visual canvas.
    """

    def __init__(self, parent, engine: ShoXxEngine, on_updated=None):
        super().__init__(parent)
        self.parent = parent
        self.engine = engine
        self.on_updated = on_updated
        self.engine.keymapper_paused_for_modal = True

        self.title("ShoXx_Emu — Widescreen Keymapping Studio (1580x1080 Landscape)")
        self.configure(bg=BG_SURFACE, highlightbackground=BORDER_FOCUS, highlightthickness=1)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"980x620+{(sw - 980) // 2}+{(sh - 620) // 2}")
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.cw = 553  # Proportional to 1580 (scale = 0.35)
        self.ch = 378  # Proportional to 1080 (scale = 0.35)
        self.scale = 0.35
        self.selected_idx = 0

        self._build_ui()
        self._refresh_list_and_canvas()

    def _on_close(self):
        self.engine.keymapper_paused_for_modal = False
        if self.on_updated:
            self.on_updated()
        self.destroy()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG_CARD, padx=20, pady=12)
        hdr.pack(fill="x")
        tk.Label(
            hdr, text="⌨  WIDESCREEN KEYMAPPING STUDIO (1580x1080 LANDSCAPE TABLET)",
            font=(FONT_UI, 12, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD
        ).pack(side="left")

        self.btn_toggle_active = tk.Button(
            hdr, text="", command=self._toggle_enabled,
            font=(FONT_UI, 9, "bold"), relief="flat", padx=14, pady=5, cursor="hand2"
        )
        self.btn_toggle_active.pack(side="right", padx=(8, 0))

        tk.Button(
            hdr, text="Reset 1580x1080 Defaults", command=self._reset_defaults,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=TEXT_SECONDARY,
            relief="flat", padx=10, pady=5, cursor="hand2"
        ).pack(side="right")

        tk.Frame(self, bg=BORDER_SUBTLE, height=1).pack(fill="x")

        body = tk.Frame(self, bg=BG_SURFACE, padx=18, pady=14)
        body.pack(fill="both", expand=True)

        # LEFT: Proportional 1580x1080 Widescreen Touch Map Canvas
        left_f = tk.Frame(body, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=12)
        left_f.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(
            left_f,
            text="1580x1080 LANDSCAPE VIEWPORT MAP (Click anywhere on canvas to move selected Key Point)",
            font=(FONT_UI, 8, "bold"), fg=ACCENT_PRIMARY, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 8))

        self.map_canvas = tk.Canvas(
            left_f, width=self.cw, height=self.ch, bg="#080C14",
            highlightthickness=1, highlightbackground=BORDER_FOCUS, cursor="crosshair"
        )
        self.map_canvas.pack()
        self.map_canvas.bind("<Button-1>", self._on_canvas_click)
        self.map_canvas.bind("<B1-Motion>", self._on_canvas_click)

        self.coord_hint_lbl = tk.Label(
            left_f,
            text="Tip: Select a key on the right, then click or drag on the 1580x1080 screen map above to position it.",
            font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_CARD
        )
        self.coord_hint_lbl.pack(anchor="w", pady=(8, 0))

        # RIGHT: Key Binding List & Custom Key Creator
        right_f = tk.Frame(body, width=350, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=12)
        right_f.pack(side="right", fill="y")
        right_f.pack_propagate(False)

        tk.Label(
            right_f, text="MAPPED PC KEYS & COORDINATES",
            font=(FONT_UI, 9, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD
        ).pack(anchor="w")

        self.keys_listbox = tk.Listbox(
            right_f, bg=BG_INPUT, fg=TEXT_PRIMARY, selectbackground=ACCENT_PRIMARY,
            font=(FONT_MONO, 9), height=12, relief="flat",
            highlightthickness=1, highlightbackground=BORDER_SUBTLE
        )
        self.keys_listbox.pack(fill="x", pady=8)
        self.keys_listbox.bind("<<ListboxSelect>>", self._on_list_select)

        # Add / Update Custom Key Form
        form = tk.Frame(right_f, bg=BG_SURFACE, padx=10, pady=8, highlightbackground=BORDER_SUBTLE, highlightthickness=1)
        form.pack(fill="x", pady=(2, 8))

        tk.Label(form, text="ADD OR UPDATE KEY BINDING", font=(FONT_UI, 8, "bold"), fg=ACCENT_PRIMARY, bg=BG_SURFACE).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))

        tk.Label(form, text="Key:", font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_SURFACE).grid(row=1, column=0, sticky="w")
        self.ent_key = tk.Entry(form, width=7, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
        self.ent_key.grid(row=1, column=1, sticky="w", padx=(4, 8))

        tk.Label(form, text="Label:", font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_SURFACE).grid(row=1, column=2, sticky="w")
        self.ent_label = tk.Entry(form, width=16, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
        self.ent_label.grid(row=1, column=3, sticky="ew", padx=(4, 0))

        tk.Label(form, text="X:", font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_SURFACE).grid(row=2, column=0, sticky="w", pady=(6, 0))
        self.ent_x = tk.Entry(form, width=7, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
        self.ent_x.grid(row=2, column=1, sticky="w", padx=(4, 8), pady=(6, 0))

        tk.Label(form, text="Y:", font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_SURFACE).grid(row=2, column=2, sticky="w", pady=(6, 0))
        self.ent_y = tk.Entry(form, width=7, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, relief="flat")
        self.ent_y.grid(row=2, column=3, sticky="w", padx=(4, 0), pady=(6, 0))

        btn_row = tk.Frame(right_f, bg=BG_CARD)
        btn_row.pack(fill="x", pady=2)
        btn_row.grid_columnconfigure((0, 1), weight=1, uniform="kmb")

        tk.Button(
            btn_row, text="+ Add / Save Key", command=self._save_or_add_key,
            font=(FONT_UI, 8, "bold"), bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY,
            relief="flat", pady=6, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 3))

        tk.Button(
            btn_row, text="Delete Selected", command=self._delete_selected_key,
            font=(FONT_UI, 8, "bold"), bg="#261216", fg=STATUS_ERR,
            relief="flat", pady=6, cursor="hand2"
        ).grid(row=0, column=1, sticky="ew", padx=(3, 0))

        tk.Button(
            right_f, text="⚡ Test Selected Key Tap on Emulator Now",
            command=self._test_selected_key,
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=STATUS_OK,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=6, cursor="hand2"
        ).pack(fill="x", pady=(6, 4))

        tk.Button(
            right_f, text="Done & Close Studio",
            command=self._on_close,
            font=(FONT_UI, 9, "bold"), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=7, cursor="hand2"
        ).pack(fill="x", side="bottom")

    def _toggle_enabled(self):
        self.engine.toggle_keymapper()
        self._refresh_list_and_canvas()

    def _reset_defaults(self):
        self.engine.reset_default_keymappings()
        self.selected_idx = 0
        self._refresh_list_and_canvas()

    def _on_list_select(self, event=None):
        sel = self.keys_listbox.curselection()
        if not sel:
            return
        self.selected_idx = sel[0]
        bindings = self.engine.keymap_config.get("bindings", [])
        if 0 <= self.selected_idx < len(bindings):
            b = bindings[self.selected_idx]
            self.ent_key.delete(0, "end")
            self.ent_key.insert(0, b.get("key", ""))
            self.ent_label.delete(0, "end")
            self.ent_label.insert(0, b.get("label", ""))
            self.ent_x.delete(0, "end")
            self.ent_x.insert(0, str(b.get("x", 790)))
            self.ent_y.delete(0, "end")
            self.ent_y.insert(0, str(b.get("y", 540)))
        self._draw_canvas()

    def _on_canvas_click(self, event):
        bindings = self.engine.keymap_config.get("bindings", [])
        if not bindings:
            return
        idx = max(0, min(len(bindings) - 1, self.selected_idx))
        real_x = max(20, min(1560, int(event.x / self.scale)))
        real_y = max(20, min(1060, int(event.y / self.scale)))
        bindings[idx]["x"] = real_x
        bindings[idx]["y"] = real_y
        self.engine.save_keymappings()
        self.ent_x.delete(0, "end")
        self.ent_x.insert(0, str(real_x))
        self.ent_y.delete(0, "end")
        self.ent_y.insert(0, str(real_y))
        self.coord_hint_lbl.config(
            text=f"✔ Updated [{bindings[idx]['key']}] ({bindings[idx].get('label', '')}) -> X={real_x}, Y={real_y}"
        )
        self._refresh_list_and_canvas(keep_selection=True)

    def _save_or_add_key(self):
        k_str = self.ent_key.get().strip().upper()
        lbl_str = self.ent_label.get().strip() or f"Custom {k_str}"
        try:
            x_val = max(10, min(1570, int(self.ent_x.get().strip())))
            y_val = max(10, min(1070, int(self.ent_y.get().strip())))
        except Exception:
            x_val, y_val = 790, 540
        if not k_str:
            return
        vk = self.engine.key_name_to_vk(k_str)
        bindings = self.engine.keymap_config.get("bindings", [])
        found_i = None
        for i, b in enumerate(bindings):
            if b.get("key", "").upper() == k_str:
                found_i = i
                break
        if found_i is not None:
            bindings[found_i]["x"] = x_val
            bindings[found_i]["y"] = y_val
            bindings[found_i]["label"] = lbl_str
            bindings[found_i]["vk"] = vk
            self.selected_idx = found_i
        else:
            bindings.append({
                "key": k_str,
                "vk": vk,
                "x": x_val,
                "y": y_val,
                "type": "tap",
                "label": lbl_str,
            })
            self.selected_idx = len(bindings) - 1
        self.engine.save_keymappings()
        self._refresh_list_and_canvas(keep_selection=True)

    def _delete_selected_key(self):
        bindings = self.engine.keymap_config.get("bindings", [])
        if 0 <= self.selected_idx < len(bindings):
            bindings.pop(self.selected_idx)
            self.selected_idx = max(0, self.selected_idx - 1)
            self.engine.save_keymappings()
            self._refresh_list_and_canvas()

    def _test_selected_key(self):
        bindings = self.engine.keymap_config.get("bindings", [])
        if 0 <= self.selected_idx < len(bindings):
            b = bindings[self.selected_idx]
            self.engine.trigger_key_action(b)
            self.coord_hint_lbl.config(text=f"⚡ Triggered test input for [{b['key']}] at ({b['x']}, {b['y']})")

    def _refresh_list_and_canvas(self, keep_selection: bool = False):
        if self.engine.keymapper_enabled:
            self.btn_toggle_active.config(text="● KEYMAPPER ACTIVE (F9)", bg=STATUS_OK, fg="#051B11")
        else:
            self.btn_toggle_active.config(text="○ ENABLE KEYMAPPER (F9)", bg=BG_INPUT, fg=TEXT_PRIMARY)

        bindings = self.engine.keymap_config.get("bindings", [])
        self.keys_listbox.delete(0, "end")
        for b in bindings:
            tag = "D-PAD" if b.get("type") == "swipe_dpad" else "TAP  "
            self.keys_listbox.insert(
                "end",
                f"[{b['key']:^5}]  ({b['x']:4d}, {b['y']:4d})  {tag}  {b.get('label', '')}"
            )
        if bindings:
            self.selected_idx = max(0, min(len(bindings) - 1, self.selected_idx))
            self.keys_listbox.selection_set(self.selected_idx)
            if not keep_selection:
                self._on_list_select()
        self._draw_canvas()

    def _draw_canvas(self):
        c = self.map_canvas
        c.delete("all")
        # Subtle grid lines representing 1580x1080 Widescreen Landscape viewport
        for gx in range(0, self.cw, 55):
            c.create_line(gx, 0, gx, self.ch, fill="#111927", width=1)
        for gy in range(0, self.ch, 45):
            c.create_line(0, gy, self.cw, gy, fill="#111927", width=1)

        c.create_text(
            10, 10,
            text="1580 x 1080 WIDESCREEN LANDSCAPE GAME VIEWPORT",
            font=(FONT_MONO, 8, "bold"), fill=TEXT_MUTED, anchor="nw"
        )

        # Draw WASD D-Pad Center Ring
        d_cx = int(self.engine.keymap_config.get("dpad_center_x", 280) * self.scale)
        d_cy = int(self.engine.keymap_config.get("dpad_center_y", 760) * self.scale)
        d_r = int(self.engine.keymap_config.get("dpad_radius", 140) * self.scale)
        c.create_oval(d_cx - d_r, d_cy - d_r, d_cx + d_r, d_cy + d_r, outline="#1E3A5F", width=2, dash=(4, 3))
        c.create_oval(d_cx - 4, d_cy - 4, d_cx + 4, d_cy + 4, fill=ACCENT_PRIMARY, outline="")

        bindings = self.engine.keymap_config.get("bindings", [])
        for idx, b in enumerate(bindings):
            px = int(b.get("x", 790) * self.scale)
            py = int(b.get("y", 540) * self.scale)
            is_sel = (idx == self.selected_idx)
            is_dpad = (b.get("type") == "swipe_dpad")

            if is_dpad:
                c.create_line(d_cx, d_cy, px, py, fill="#1D4ED8", width=1)

            r = 16 if is_sel else 13
            ring_col = "#00F0FF" if is_sel else (STATUS_OK if not is_dpad else ACCENT_PRIMARY)
            fill_col = "#172554" if is_sel else "#0F172A"

            c.create_oval(px - r, py - r, px + r, py + r, fill=fill_col, outline=ring_col, width=2 if is_sel else 1)
            c.create_text(px, py, text=b.get("key", "?"), font=(FONT_MONO, 8, "bold"), fill=TEXT_PRIMARY)
            c.create_text(px, py + r + 9, text=f"{b['x']},{b['y']}", font=(FONT_MONO, 7), fill=TEXT_SECONDARY)


class ShoXxApp(tk.Tk):
    """
    Professional Fullscreen Studio Control Center with Fixed Right-Side GAMING EXTEND Dock Panel.
    """

    def __init__(self, auto_boot: bool = False):
        super().__init__()
        self.title("ShoXx_Emu Studio — Portable Android 15 / 16 / 17 Workstation")
        self.configure(bg=BG_ROOT)

        self.attributes("-fullscreen", True)
        self.is_fullscreen = True
        self.bind("<F11>", self.toggle_app_fullscreen)
        self.bind("<F10>", self.toggle_sidebar_collapse)
        self.bind("<F9>", self.toggle_keymapper_hotkey)
        self.bind("<Escape>", self.on_escape_key)

        ico_path = os.path.join(BASE_DIR, "assets", "shoxx_icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()
        self.geometry(f"{self.sw}x{self.sh}+0+0")

        self.auto_boot_requested = auto_boot
        self.anim_tick = 0.0
        self.progress_pct = 100.0
        self.progress_status = "System Ready — Portable Stealth Environment Verified"
        self.is_busy = False

        self.engine = ShoXxEngine(
            log_callback=self.append_log_threadsafe,
            progress_callback=self.update_progress_threadsafe
        )
        self.showing_emulator_frame = False
        self.engine.on_window_embedded_cb = lambda: self.after(0, self.show_emulator_viewport_frame)
        self.sys_report = self.engine.analyze_system_hardware()
        self.plugins_list = self.engine.inspect_plugins_and_tools()

        opt = self.sys_report["optimal"]
        self.engine.cores = opt["cores"]
        self.engine.ram_mb = opt["ram_mb"]
        self.engine.gpu_mode = opt["gpu_mode"]
        self.engine.resolution = opt["resolution"]
        self.engine.dpi = opt["dpi"]

        self._build_dashboard_ui()
        self.after(150, self._setup_native_win32_file_drop)
        self.splash = ExecutiveSplashOverlay(self, self.engine, on_complete=self._on_splash_finished)

    def toggle_app_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def on_escape_key(self, event=None):
        if hasattr(self, "splash") and self.splash and self.splash.running:
            self.splash.finish()

    def _on_splash_finished(self):
        sr = self.sys_report
        opt = sr["optimal"]
        prof = self.engine.get_active_profile()
        self.append_log(f"Active Profile: '{prof['name']}' (IMEI: {prof['imei']} | Retail Stealth: Enabled)", "INFO")
        self.append_log(
            f"Hardware Telemetry: {sr['cpu_name']} | {sr['ram_total_mb']} MB RAM | {sr['primary_gpu']['name']}",
            "INFO"
        )
        self.append_log(f"Recommended Profile Applied: {opt['cores']} Cores, {opt['ram_mb']} MB RAM, GPU '{opt['gpu_mode']}'", "SUCCESS")
        self.refresh_component_badges()
        self._animate_dashboard()

        st = self.engine.check_component_status(self.engine.selected_android)
        if not st["all_ready"]:
            self.append_log(f"Autonomous Setup: Configuring Android {self.engine.selected_android} AVD container...", "CYBER")
            self.start_one_click_setup(auto_launch_after=self.auto_boot_requested)
        elif self.auto_boot_requested:
            self.append_log("Auto-Boot: Launching Pixel 9 Pro XL in Fullscreen...", "ROOT")
            self.start_emulator_launch()

    def _build_dashboard_ui(self):
        """
        Clean, structured 2-zone Fullscreen Layout:
        - Right Docked Sidebar (SIDEBAR_WIDTH): GAMING EXTEND Controls, Android Navigation, Task Manager, APK/XAPK & Shared Folder
        - Left Main Studio Area: Executive Top Bar + 2 Balanced Columns + Subtle Status Footer
        """
        # ==================== RIGHT DOCKED GAMING EXTEND SIDEBAR ====================
        self.gaming_sidebar = tk.Frame(
            self, width=SIDEBAR_WIDTH, bg=BG_SIDEBAR,
            highlightbackground=BORDER_SUBTLE, highlightthickness=1
        )
        self.gaming_sidebar.pack(side="right", fill="y")
        self.gaming_sidebar.pack_propagate(False)
        self._build_gaming_extend_sidebar(self.gaming_sidebar)

        # ==================== LEFT / MAIN STUDIO WORKSPACE ====================
        main_work = tk.Frame(self, bg=BG_ROOT)
        main_work.pack(side="left", fill="both", expand=True)

        # Clean Top Navigation Bar (Expanded to accommodate 150% larger top-left neon logo)
        top_bar = tk.Frame(main_work, bg=BG_SURFACE, height=130, padx=24)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        title_box = tk.Frame(top_bar, bg=BG_SURFACE)
        title_box.pack(side="left", fill="y", pady=6)

        # Top-Left Logo from D:\SHOXX_EMU_26\splash.jpg (150% larger: 220x115)
        self.top_logo_photo = None
        self.window_icon_photo = None
        logo_path = os.path.join(BASE_DIR, "splash.jpg")
        if not os.path.isfile(logo_path):
            logo_path = os.path.join(BASE_DIR, "assets", "splash_graffiti.png")
        if os.path.isfile(logo_path):
            try:
                raw_logo = Image.open(logo_path).convert("RGB")
                logo_thumb = raw_logo.resize((220, 115), Image.Resampling.LANCZOS)
                self.top_logo_photo = ImageTk.PhotoImage(logo_thumb)
                icon_thumb = raw_logo.resize((64, 64), Image.Resampling.LANCZOS)
                self.window_icon_photo = ImageTk.PhotoImage(icon_thumb)
                self.iconphoto(False, self.window_icon_photo)

                self.top_logo_lbl = tk.Label(
                    title_box, image=self.top_logo_photo, bg=BG_CARD,
                    bd=0, highlightthickness=2, highlightbackground="#00D8FF",
                    cursor="hand2"
                )
                self.top_logo_lbl.pack(side="left", padx=(0, 16))
                self.top_logo_lbl.bind("<Button-1>", lambda e: self.replay_splash_overlay())
            except Exception:
                pass

        tk.Label(
            title_box, text="ShoXx_Emu",
            font=(FONT_UI, 18, "bold"), fg=TEXT_PRIMARY, bg=BG_SURFACE
        ).pack(side="left")
        tk.Label(
            title_box, text="  STUDIO ENTERPRISE  •  PORTABLE STEALTH SMARTPHONE WORKSTATION",
            font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_SURFACE
        ).pack(side="left", padx=(8, 0))

        # Top-Right Action Buttons
        nav_btns = tk.Frame(top_bar, bg=BG_SURFACE)
        nav_btns.pack(side="right", pady=46)

        self.btn_toggle_view = tk.Button(
            nav_btns, text="⊞ Emulator Frame", command=self.toggle_studio_viewport_mode,
            font=(FONT_UI, 9, "bold"), bg=BG_CARD, fg=STATUS_OK,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=12, pady=5, cursor="hand2"
        )
        self.btn_toggle_view.pack(side="left", padx=4)

        self.btn_top_keymapper = tk.Button(
            nav_btns, text="⌨ Keymapper (F9)", command=self.open_keymapper_modal,
            font=(FONT_UI, 9, "bold"), bg=BG_CARD, fg=ACCENT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=12, pady=5, cursor="hand2"
        )
        self.btn_top_keymapper.pack(side="left", padx=4)

        tk.Button(
            nav_btns, text="Profiles & ROMs", command=self.open_profile_manager_modal,
            font=(FONT_UI, 9, "bold"), bg=BG_CARD, fg=TEXT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=12, pady=5, cursor="hand2"
        ).pack(side="left", padx=4)

        tk.Button(
            nav_btns, text="Git Update", command=self._on_git_update_clicked,
            font=(FONT_UI, 9, "bold"), bg=BG_CARD, fg=ACCENT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=12, pady=5, cursor="hand2"
        ).pack(side="left", padx=4)

        tk.Button(
            nav_btns, text="Diagnostics", command=self._replay_splash,
            font=(FONT_UI, 9), bg=BG_CARD, fg=TEXT_SECONDARY,
            activebackground=BG_INPUT, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=12, pady=5, cursor="hand2"
        ).pack(side="left", padx=4)

        tk.Button(
            nav_btns, text="Window / Fullscreen (F11)", command=self.toggle_app_fullscreen,
            font=(FONT_UI, 9), bg=BG_CARD, fg=TEXT_SECONDARY,
            activebackground=BG_INPUT, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=12, pady=5, cursor="hand2"
        ).pack(side="left", padx=4)

        tk.Button(
            nav_btns, text="Exit", command=self.on_close,
            font=(FONT_UI, 9, "bold"), bg="#261216", fg=STATUS_ERR,
            activebackground=STATUS_ERR, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground="#451A22",
            relief="flat", padx=14, pady=5, cursor="hand2"
        ).pack(side="left", padx=(4, 0))

        tk.Frame(main_work, bg=BORDER_SUBTLE, height=1).pack(fill="x")

        # Subtle Bottom Progress & Status Footer (Packed before central workspace so it stays anchored at bottom)
        self.footer_canvas = tk.Canvas(main_work, height=38, bg=BG_SURFACE, highlightthickness=0)
        self.footer_canvas.pack(fill="x", side="bottom")

        # ==================== EMBEDDED STUDIO EMULATOR CONTAINER FRAME ====================
        self.emulator_viewport_frame = tk.Frame(
            main_work, bg=BG_SURFACE,
            highlightbackground=BORDER_FOCUS, highlightthickness=2
        )

        emu_hdr = tk.Frame(self.emulator_viewport_frame, bg=BG_CARD, height=38, padx=12)
        emu_hdr.pack(fill="x", side="top")
        emu_hdr.pack_propagate(False)

        self.emu_frame_title_lbl = tk.Label(
            emu_hdr,
            text="●  ANDROID EMULATOR STUDIO FRAME — Google Pixel Tablet (Landscape 16:9)",
            font=(FONT_UI, 9, "bold"), fg=STATUS_OK, bg=BG_CARD
        )
        self.emu_frame_title_lbl.pack(side="left", pady=8)

        emu_f_btns = tk.Frame(emu_hdr, bg=BG_CARD)
        emu_f_btns.pack(side="right", pady=5)

        tk.Button(
            emu_f_btns, text="⊞ Studio Dashboard",
            command=self.show_studio_dashboard,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            activebackground=ACCENT_PRIMARY, relief="flat", padx=10, pady=3, cursor="hand2"
        ).pack(side="left", padx=3)

        tk.Button(
            emu_f_btns, text="▶ Play Store",
            command=self.engine.open_google_play_store,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=STATUS_OK,
            relief="flat", padx=8, pady=3, cursor="hand2"
        ).pack(side="left", padx=3)

        tk.Button(
            emu_f_btns, text="🌐 Chrome",
            command=self.engine.open_google_chrome,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=ACCENT_PRIMARY,
            relief="flat", padx=8, pady=3, cursor="hand2"
        ).pack(side="left", padx=3)

        self.btn_hdr_keymapper = tk.Button(
            emu_f_btns, text="⌨ Keymap (F9)",
            command=self.open_keymapper_modal,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=ACCENT_PRIMARY,
            relief="flat", padx=8, pady=3, cursor="hand2"
        )
        self.btn_hdr_keymapper.pack(side="left", padx=3)

        tk.Button(
            emu_f_btns, text="↻ 16:9 Landscape",
            command=self.engine.force_landscape_tablet_mode,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=STATUS_OK,
            relief="flat", padx=8, pady=3, cursor="hand2"
        ).pack(side="left", padx=3)

        self.btn_undock_embed = tk.Button(
            emu_f_btns, text="❐ Undock Window",
            command=self.toggle_embed_or_undock,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=ACCENT_PRIMARY,
            relief="flat", padx=10, pady=3, cursor="hand2"
        )
        self.btn_undock_embed.pack(side="left", padx=3)

        tk.Button(
            emu_f_btns, text="─ Minimize",
            command=self._minimize_emulator_or_studio,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            relief="flat", padx=10, pady=3, cursor="hand2"
        ).pack(side="left", padx=3)

        tk.Button(
            emu_f_btns, text="□ Max Width (F10)",
            command=self.toggle_sidebar_collapse,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            relief="flat", padx=10, pady=3, cursor="hand2"
        ).pack(side="left", padx=3)

        tk.Button(
            emu_f_btns, text="✕ Stop",
            command=self._stop_and_return_to_dashboard,
            font=(FONT_UI, 8, "bold"), bg="#261216", fg=STATUS_ERR,
            activebackground=STATUS_ERR, activeforeground=TEXT_PRIMARY,
            relief="flat", padx=10, pady=3, cursor="hand2"
        ).pack(side="left", padx=(3, 0))

        tk.Frame(self.emulator_viewport_frame, bg=BORDER_SUBTLE, height=1).pack(fill="x")

        self.emu_host_container = tk.Frame(self.emulator_viewport_frame, bg="#05070B")
        self.emu_host_container.pack(fill="both", expand=True)
        self.emu_host_container.bind("<Configure>", self._on_emu_container_resized)

        self.emu_placeholder_lbl = tk.Label(
            self.emu_host_container,
            text="Launching & Embedding Google Pixel Tablet (Landscape 16:9) inside Studio Frame...\n"
                 "Use the frame header bar above to [─ Minimize], [□ Max Width], [❐ Undock], or return to [⊞ Studio Dashboard].",
            font=(FONT_UI, 10), fg=TEXT_SECONDARY, bg="#05070B", justify="center"
        )
        self.emu_placeholder_lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Main 2-Column Content Area (Studio Dashboard)
        body = tk.Frame(main_work, bg=BG_ROOT)
        self.dashboard_body = body
        body.pack(fill="both", expand=True, padx=20, pady=16)
        body.grid_columnconfigure(0, weight=5, uniform="mcol")
        body.grid_columnconfigure(1, weight=5, uniform="mcol")
        body.grid_rowconfigure(0, weight=1)

        # ==================== LEFT COLUMN: PROFILE, OS VERSION, ROOT ARCHITECTURE & LAUNCH ====================
        col0 = tk.Frame(body, bg=BG_SURFACE, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=18, pady=16)
        col0.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 1. Active Profile Card
        prof_hdr = tk.Frame(col0, bg=BG_SURFACE)
        prof_hdr.pack(fill="x", pady=(0, 6))
        tk.Label(
            prof_hdr, text="ACTIVE EMULATOR PROFILE",
            font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_SURFACE
        ).pack(side="left")
        tk.Button(
            prof_hdr, text="Manage Profiles...", command=self.open_profile_manager_modal,
            font=(FONT_UI, 8, "bold"), bg=BG_CARD, fg=ACCENT_PRIMARY,
            relief="flat", padx=8, pady=2, cursor="hand2"
        ).pack(side="right")

        prof_card = tk.Frame(col0, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=14, pady=10)
        prof_card.pack(fill="x", pady=(0, 14))

        self.active_prof_lbl = tk.Label(
            prof_card, text=self.engine.get_active_profile()["name"],
            font=(FONT_UI, 11, "bold"), fg=TEXT_PRIMARY, bg=BG_CARD, anchor="w"
        )
        self.active_prof_lbl.pack(fill="x")

        p_curr = self.engine.get_active_profile()
        pix_c = PIXEL_PROFILES.get(p_curr.get("pixel_model", "pixel_tablet"), PIXEL_PROFILES["pixel_tablet"])
        self.active_prof_sub = tk.Label(
            prof_card,
            text=f"Stealth Identity: {pix_c['manufacturer']} {pix_c['model']} ({pix_c['device']} • Landscape)  •  IMEI: {p_curr.get('imei')}  •  Carrier: {p_curr.get('carrier', 'Telekom.de')}",
            font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_CARD, anchor="w"
        )
        self.active_prof_sub.pack(fill="x", pady=(2, 0))

        # 2. Android OS Version Selection (15 / 16 / 17 with Google Play Store)
        os_hdr = tk.Frame(col0, bg=BG_SURFACE)
        os_hdr.pack(fill="x", pady=(0, 6))
        tk.Label(
            os_hdr, text="ANDROID OPERATING SYSTEM (GOOGLE PLAY STORE INCLUDED)",
            font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_SURFACE
        ).pack(side="left")
        tk.Button(
            os_hdr, text="Download Play Store ROM", command=self._download_selected_playstore_rom,
            font=(FONT_UI, 8), bg=BG_CARD, fg=TEXT_SECONDARY,
            relief="flat", padx=8, pady=2, cursor="hand2"
        ).pack(side="right")

        os_btn_row = tk.Frame(col0, bg=BG_SURFACE)
        os_btn_row.pack(fill="x", pady=(0, 14))
        os_btn_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="osbtn")

        self.os_buttons = {}
        for idx, (ver_key, label_txt) in enumerate([
            ("15", "Android 15\nAPI 35 • Play Store"),
            ("16", "Android 16\nAPI 36 • Play Store"),
            ("17", "Android 17\nAPI 37 • Play Store")
        ]):
            btn = tk.Button(
                os_btn_row, text=label_txt,
                command=lambda v=ver_key: self.select_android_version(v),
                font=(FONT_UI, 9, "bold"), relief="flat", pady=8, cursor="hand2"
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=(0 if idx == 0 else 4, 0 if idx == 2 else 4))
            self.os_buttons[ver_key] = btn
        self._update_os_button_styles()

        # 3. Root Architecture & Switch
        root_hdr = tk.Frame(col0, bg=BG_SURFACE)
        root_hdr.pack(fill="x", pady=(0, 6))
        self.root_status_lbl = tk.Label(
            root_hdr, text="SUPERUSER ROOT ACCESS: ENABLED (Magisk v31.1)",
            font=(FONT_UI, 9, "bold"), fg=STATUS_OK, bg=BG_SURFACE
        )
        self.root_status_lbl.pack(side="left")

        self.root_toggle_btn = tk.Button(
            root_hdr, text="Root: ON", command=self.toggle_root_access,
            font=(FONT_UI, 8, "bold"), bg=STATUS_OK, fg=BG_ROOT,
            relief="flat", padx=12, pady=2, cursor="hand2"
        )
        self.root_toggle_btn.pack(side="right")

        rm_btn_row = tk.Frame(col0, bg=BG_SURFACE)
        rm_btn_row.pack(fill="x", pady=(0, 14))
        rm_btn_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="rmbtn")

        self.rm_buttons = {}
        for idx, (rm_key, rm_txt) in enumerate([
            ("MAGISK", "1. Magisk v31.1\nZygisk & Systemless"),
            ("KERNELSU", "2. KernelSU v3.3\nKernel ksud Bridge"),
            ("APATCH_SU", "3. APatch + SU\nNative R/W Bridge")
        ]):
            btn = tk.Button(
                rm_btn_row, text=rm_txt,
                command=lambda m=rm_key: self.select_root_method(m),
                font=(FONT_UI, 9, "bold"), relief="flat", pady=8, cursor="hand2"
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=(0 if idx == 0 else 4, 0 if idx == 2 else 4))
            self.rm_buttons[rm_key] = btn
        self._update_root_method_styles()

        # 4. Component & Plugin Readiness Matrix
        tk.Label(
            col0, text="PORTABLE SDK & MODULE STATUS",
            font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_SURFACE
        ).pack(anchor="w", pady=(0, 6))

        self.plugins_canvas = tk.Canvas(col0, height=195, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        self.plugins_canvas.pack(fill="both", expand=True, pady=(0, 14))

        # 5. Primary Launch & Auto-Setup Buttons
        btn_row = tk.Frame(col0, bg=BG_SURFACE)
        btn_row.pack(fill="x", side="bottom")

        self.btn_oneclick = tk.Button(
            btn_row,
            text="Verify & Auto-Setup SDK",
            command=lambda: self.start_one_click_setup(auto_launch_after=False),
            font=(FONT_UI, 9, "bold"), bg=BG_CARD, fg=TEXT_PRIMARY,
            activebackground=BG_INPUT, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=14, pady=11, cursor="hand2"
        )
        self.btn_oneclick.pack(side="left", padx=(0, 8))

        self.btn_launch = tk.Button(
            btn_row,
            text="Launch Pixel 9 Pro XL in Fullscreen",
            command=self.start_emulator_launch,
            font=(FONT_UI, 10, "bold"), bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY,
            activebackground=ACCENT_HOVER, activeforeground=TEXT_PRIMARY,
            relief="flat", pady=11, cursor="hand2"
        )
        self.btn_launch.pack(side="left", fill="x", expand=True)

        # ==================== RIGHT COLUMN: SYSTEM TELEMETRY, HARDWARE CONFIG & CONSOLE ====================
        col1 = tk.Frame(body, bg=BG_SURFACE, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=18, pady=16)
        col1.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        sys_hdr = tk.Frame(col1, bg=BG_SURFACE)
        sys_hdr.pack(fill="x", pady=(0, 6))
        tk.Label(
            sys_hdr, text="SYSTEM HARDWARE TELEMETRY & OPTIMAL SETTINGS",
            font=(FONT_UI, 9, "bold"), fg=TEXT_SECONDARY, bg=BG_SURFACE
        ).pack(side="left")
        tk.Button(
            sys_hdr, text="Apply Optimal Settings", command=self.apply_optimal_settings_clicked,
            font=(FONT_UI, 8, "bold"), bg=BG_CARD, fg=STATUS_OK,
            relief="flat", padx=8, pady=2, cursor="hand2"
        ).pack(side="right")

        self.sys_canvas = tk.Canvas(col1, height=225, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_SUBTLE)
        self.sys_canvas.pack(fill="x", pady=(0, 12))

        # Hardware & Stealth Model Selector Row
        hw_card = tk.Frame(col1, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=10)
        hw_card.pack(fill="x", pady=(0, 12))

        s_row = tk.Frame(hw_card, bg=BG_CARD)
        s_row.pack(fill="x", pady=2)
        tk.Label(s_row, text="Stealth Device:", font=(FONT_UI, 9), fg=TEXT_SECONDARY, bg=BG_CARD, width=14, anchor="w").pack(side="left")
        self.pixel_var = tk.StringVar(value=PIXEL_PROFILES[self.engine.selected_pixel]["display"])
        pixel_menu = tk.OptionMenu(s_row, self.pixel_var, *[p["display"] for p in PIXEL_PROFILES.values()], command=self._on_hw_changed)
        pixel_menu.config(bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_UI, 9), highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat")
        pixel_menu.pack(side="left", fill="x", expand=True)

        mc_row = tk.Frame(hw_card, bg=BG_CARD)
        mc_row.pack(fill="x", pady=(6, 2))
        tk.Label(mc_row, text="RAM / Cores:", font=(FONT_UI, 9), fg=TEXT_SECONDARY, bg=BG_CARD, width=14, anchor="w").pack(side="left")
        opt = self.sys_report["optimal"]
        self.ram_var = tk.StringVar(value=opt["ram_label"])
        ram_menu = tk.OptionMenu(mc_row, self.ram_var, "2048 MB (2 GB)", "4096 MB (4 GB)", "6144 MB (6 GB)", "8192 MB (8 GB)", command=self._on_hw_changed)
        ram_menu.config(bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_UI, 9), highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat")
        ram_menu.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.cores_var = tk.StringVar(value=opt["cores_label"])
        cores_menu = tk.OptionMenu(mc_row, self.cores_var, "2 Cores", "4 Cores (Turbo)", "6 Cores (Extreme)", "8 Cores (Max)", command=self._on_hw_changed)
        cores_menu.config(bg=BG_INPUT, fg=TEXT_PRIMARY, font=(FONT_UI, 9), highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat")
        cores_menu.pack(side="left", fill="x", expand=True)

        # Live Telemetry Status Strip
        self.tele_lbl = tk.Label(
            col1,
            text="Target: Pixel 9 Pro XL (komodo)  •  OS: Android 16 (Play Store)  •  Root: Magisk v31.1",
            font=(FONT_MONO, 8), fg=ACCENT_PRIMARY, bg=BG_SURFACE, anchor="w"
        )
        self.tele_lbl.pack(fill="x", pady=(0, 4))

        # Clean Console Log Output
        log_frame = tk.Frame(col1, bg=BG_INPUT, highlightbackground=BORDER_SUBTLE, highlightthickness=1)
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame, bg=BG_INPUT, fg=TEXT_SECONDARY,
            font=(FONT_MONO, 9), insertbackground=ACCENT_PRIMARY,
            relief="flat", wrap="word", padx=10, pady=8
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(log_frame, command=self.log_text.yview, bg=BG_SURFACE)
        sb.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=sb.set)

        self.log_text.tag_config("INFO", foreground=TEXT_SECONDARY)
        self.log_text.tag_config("CYBER", foreground=ACCENT_PRIMARY)
        self.log_text.tag_config("SUCCESS", foreground=STATUS_OK)
        self.log_text.tag_config("ROOT", foreground=TEXT_PRIMARY)
        self.log_text.tag_config("WARN", foreground=STATUS_WARN)
        self.log_text.tag_config("ERROR", foreground=STATUS_ERR)

        self._update_launch_button_caption()

    # =========================================================================
    # FIXED RIGHT-SIDE "GAMING EXTEND" SIDEBAR PANEL (CLEAN & PROFESSIONAL)
    # =========================================================================

    def _build_gaming_extend_sidebar(self, parent):
        # Container for Expanded Mode (340px)
        self.sidebar_expanded_frame = tk.Frame(parent, bg=BG_SIDEBAR)
        self.sidebar_expanded_frame.pack(fill="both", expand=True)

        # Container for Collapsed Slim-Dock Mode (48px)
        self.sidebar_collapsed_frame = tk.Frame(parent, bg=BG_SIDEBAR)

        # ---- BUILD COLLAPSED SLIM-DOCK STRIP (48px) ----
        tk.Button(
            self.sidebar_collapsed_frame, text="⟪",
            command=self.toggle_sidebar_collapse,
            font=(FONT_UI, 11, "bold"), bg=BG_SURFACE, fg=ACCENT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            relief="flat", pady=12, cursor="hand2"
        ).pack(fill="x")
        tk.Frame(self.sidebar_collapsed_frame, bg=BORDER_SUBTLE, height=1).pack(fill="x", pady=(0, 8))

        slim_actions = [
            ("◀", lambda: self.engine.send_nav_key(4, "BACK"), TEXT_PRIMARY),
            ("⏺", lambda: self.engine.send_nav_key(3, "HOME"), TEXT_PRIMARY),
            ("▣", self._on_recents_clicked, TEXT_PRIMARY),
            ("＋", lambda: self.engine.send_nav_key(24, "VOL+"), TEXT_SECONDARY),
            ("－", lambda: self.engine.send_nav_key(25, "VOL-"), TEXT_SECONDARY),
            ("▶", self.engine.open_google_play_store, ACCENT_PRIMARY),
            ("📦", self.browse_and_install_apk_or_xapk, ACCENT_PRIMARY),
            ("📂", self.pick_and_copy_file_to_emulator, TEXT_PRIMARY),
            ("─", lambda: self.engine.control_emulator_window("minimize"), TEXT_PRIMARY),
            ("□", lambda: self.engine.control_emulator_window("maximize"), TEXT_PRIMARY),
            ("❐", lambda: self.engine.control_emulator_window("restore_dock"), ACCENT_PRIMARY),
            ("■", self.engine.stop_emulator, STATUS_ERR),
        ]
        for sym, cmd, fg_c in slim_actions:
            tk.Button(
                self.sidebar_collapsed_frame, text=sym, command=cmd,
                font=(FONT_UI, 10, "bold"), bg=BG_CARD, fg=fg_c,
                activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
                highlightthickness=1, highlightbackground=BORDER_SUBTLE,
                relief="flat", pady=7, cursor="hand2"
            ).pack(fill="x", padx=5, pady=3)

        # ---- BUILD EXPANDED FULL GAMING EXTEND SIDEBAR (340px) ----
        exp = self.sidebar_expanded_frame
        hdr = tk.Frame(exp, bg=BG_SURFACE, pady=12, padx=14)
        hdr.pack(fill="x")

        hdr_top = tk.Frame(hdr, bg=BG_SURFACE)
        hdr_top.pack(fill="x")
        tk.Label(
            hdr_top, text="GAMING EXTEND",
            font=(FONT_UI, 11, "bold"), fg=TEXT_PRIMARY, bg=BG_SURFACE
        ).pack(side="left")
        tk.Button(
            hdr_top, text="⟫  Collapse (F10)",
            command=self.toggle_sidebar_collapse,
            font=(FONT_UI, 8, "bold"), bg=BG_CARD, fg=TEXT_SECONDARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", padx=8, pady=2, cursor="hand2"
        ).pack(side="right")

        tk.Label(
            hdr, text="Docked Fullscreen Control Bar",
            font=(FONT_UI, 8), fg=TEXT_SECONDARY, bg=BG_SURFACE
        ).pack(anchor="w", pady=(2, 0))

        tk.Frame(exp, bg=BORDER_SUBTLE, height=1).pack(fill="x")

        # 1. ANDROID NAVIGATION KEYS (ZURÜCK, HOME, APPS)
        nav_card = tk.Frame(exp, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=10)
        nav_card.pack(fill="x", padx=12, pady=(12, 8))

        tk.Label(
            nav_card, text="ANDROID NAVIGATION",
            font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 6))

        nav_row = tk.Frame(nav_card, bg=BG_CARD)
        nav_row.pack(fill="x")
        nav_row.grid_columnconfigure((0, 1, 2), weight=1, uniform="navb")

        tk.Button(
            nav_row, text="◀  Back",
            command=lambda: self.engine.send_nav_key(4, "BACK"),
            font=(FONT_UI, 9, "bold"), bg=BG_INPUT, fg=TEXT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=8, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 3))

        tk.Button(
            nav_row, text="⏺  Home",
            command=lambda: self.engine.send_nav_key(3, "HOME"),
            font=(FONT_UI, 9, "bold"), bg=BG_INPUT, fg=TEXT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=8, cursor="hand2"
        ).grid(row=0, column=1, sticky="ew", padx=3)

        tk.Button(
            nav_row, text="▣  Apps",
            command=self._on_recents_clicked,
            font=(FONT_UI, 9, "bold"), bg=BG_INPUT, fg=TEXT_PRIMARY,
            activebackground=ACCENT_PRIMARY, activeforeground=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=8, cursor="hand2"
        ).grid(row=0, column=2, sticky="ew", padx=(3, 0))

        vp_row = tk.Frame(nav_card, bg=BG_CARD)
        vp_row.pack(fill="x", pady=(6, 0))
        vp_row.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="vpb")
        tk.Button(vp_row, text="Vol +", command=lambda: self.engine.send_nav_key(24, "VOL+"), font=(FONT_UI, 8), bg=BG_SURFACE, fg=TEXT_SECONDARY, relief="flat", pady=4, cursor="hand2").grid(row=0, column=0, sticky="ew", padx=(0, 2))
        tk.Button(vp_row, text="Vol -", command=lambda: self.engine.send_nav_key(25, "VOL-"), font=(FONT_UI, 8), bg=BG_SURFACE, fg=TEXT_SECONDARY, relief="flat", pady=4, cursor="hand2").grid(row=0, column=1, sticky="ew", padx=2)
        tk.Button(vp_row, text="▶ Play Store", command=self.engine.open_google_play_store, font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=STATUS_OK, relief="flat", pady=4, cursor="hand2").grid(row=0, column=2, sticky="ew", padx=2)
        tk.Button(vp_row, text="🌐 Chrome", command=self.engine.open_google_chrome, font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=ACCENT_PRIMARY, relief="flat", pady=4, cursor="hand2").grid(row=0, column=3, sticky="ew", padx=(2, 0))

        hs_row = tk.Frame(nav_card, bg=BG_CARD)
        hs_row.pack(fill="x", pady=(5, 0))
        hs_row.grid_columnconfigure((0, 1), weight=1, uniform="hsb")
        tk.Button(
            hs_row, text="★ Pin Play Store & Chrome",
            command=self.engine.setup_homescreen_playstore_and_chrome,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=4, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 3))

        self.btn_sb_keymapper = tk.Button(
            hs_row, text="⌨ Keymapper (F9)",
            command=self.open_keymapper_modal,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=ACCENT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=4, cursor="hand2"
        )
        self.btn_sb_keymapper.grid(row=0, column=1, sticky="ew", padx=(3, 0))

        # 2. BACKGROUND APPS TASK MANAGER
        bg_card = tk.Frame(exp, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=10)
        bg_card.pack(fill="x", padx=12, pady=6)

        bg_hdr = tk.Frame(bg_card, bg=BG_CARD)
        bg_hdr.pack(fill="x")
        tk.Label(bg_hdr, text="RUNNING BACKGROUND APPS", font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD).pack(side="left")
        tk.Button(
            bg_hdr, text="Refresh", command=self.refresh_background_apps_list,
            font=(FONT_UI, 8), bg=BG_SURFACE, fg=ACCENT_PRIMARY, relief="flat", padx=6, cursor="hand2"
        ).pack(side="right")

        self.bg_apps_listbox = tk.Listbox(
            bg_card, bg=BG_INPUT, fg=TEXT_PRIMARY, selectbackground=ACCENT_PRIMARY,
            font=(FONT_MONO, 8), height=4, relief="flat", highlightthickness=1, highlightbackground=BORDER_SUBTLE
        )
        self.bg_apps_listbox.pack(fill="x", pady=6)
        self.bg_apps_listbox.insert("end", "Click 'Apps' or 'Refresh' when active")

        tk.Button(
            bg_card, text="Force Stop Selected App", command=self.kill_selected_bg_app,
            font=(FONT_UI, 8, "bold"), bg=BG_SURFACE, fg=STATUS_WARN,
            activebackground=STATUS_ERR, activeforeground=TEXT_PRIMARY, relief="flat", pady=5, cursor="hand2"
        ).pack(fill="x")

        # 3. APK & XAPK PACKAGE INSTALLER
        apk_card = tk.Frame(exp, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=10)
        apk_card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            apk_card, text="APK & XAPK INSTALLER",
            font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD
        ).pack(anchor="w")
        tk.Label(
            apk_card, text="Supports .apk, .xapk (Split + OBB), .apkm  •  Drag & Drop Ready",
            font=(FONT_UI, 8), fg=TEXT_MUTED, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 6))

        tk.Button(
            apk_card, text="Install APK / XAPK File...",
            command=self.browse_and_install_apk_or_xapk,
            font=(FONT_UI, 9, "bold"), bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY,
            activebackground=ACCENT_HOVER, relief="flat", pady=7, cursor="hand2"
        ).pack(fill="x")

        # 4. SHARED PC <-> EMULATOR FOLDER
        sh_card = tk.Frame(exp, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=10)
        sh_card.pack(fill="x", padx=12, pady=6)

        tk.Label(
            sh_card, text="SHARED FOLDER (PC ↔ EMULATOR)",
            font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD
        ).pack(anchor="w")
        tk.Label(
            sh_card, text="./Shared_PC_Folder ↔ /sdcard/Download/ShoXx_Shared (Drag & Drop)",
            font=(FONT_UI, 8), fg=TEXT_MUTED, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 6))

        tk.Button(
            sh_card, text="Copy File from PC to Emulator...",
            command=self.pick_and_copy_file_to_emulator,
            font=(FONT_UI, 9, "bold"), bg=BG_INPUT, fg=TEXT_PRIMARY,
            activebackground=ACCENT_PRIMARY, highlightthickness=1, highlightbackground=BORDER_SUBTLE,
            relief="flat", pady=6, cursor="hand2"
        ).pack(fill="x", pady=(0, 4))

        sh_row = tk.Frame(sh_card, bg=BG_CARD)
        sh_row.pack(fill="x", pady=2)
        sh_row.grid_columnconfigure((0, 1), weight=1, uniform="shb")

        tk.Button(
            sh_row, text="Sync PC → Emu",
            command=lambda: self.engine.sync_shared_folder_to_emulator(None),
            font=(FONT_UI, 8), bg=BG_SURFACE, fg=TEXT_PRIMARY, relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 3))

        tk.Button(
            sh_row, text="Pull Emu → PC",
            command=self.engine.pull_shared_folder_from_emulator,
            font=(FONT_UI, 8), bg=BG_SURFACE, fg=TEXT_PRIMARY, relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=1, sticky="ew", padx=(3, 0))

        tk.Button(
            sh_card, text="Open PC Shared Folder",
            command=self.engine.open_pc_shared_folder_explorer,
            font=(FONT_UI, 8), bg=BG_SURFACE, fg=TEXT_SECONDARY, relief="flat", pady=5, cursor="hand2"
        ).pack(fill="x", pady=(4, 0))

        # 5. EMULATOR WINDOW FRAME & STEALTH CONTROLS
        st_card = tk.Frame(exp, bg=BG_CARD, highlightbackground=BORDER_SUBTLE, highlightthickness=1, padx=12, pady=10)
        st_card.pack(fill="both", expand=True, padx=12, pady=(6, 12))

        tk.Label(
            st_card, text="EMULATOR WINDOW FRAME & STEALTH",
            font=(FONT_UI, 8, "bold"), fg=TEXT_SECONDARY, bg=BG_CARD
        ).pack(anchor="w", pady=(0, 4))

        win_row = tk.Frame(st_card, bg=BG_CARD)
        win_row.pack(fill="x", pady=(0, 6))
        win_row.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="winb")

        tk.Button(
            win_row, text="─ Min",
            command=lambda: self.engine.control_emulator_window("minimize"),
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=0, sticky="ew", padx=(0, 2))

        tk.Button(
            win_row, text="□ Max",
            command=lambda: self.engine.control_emulator_window("maximize"),
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=1, sticky="ew", padx=2)

        tk.Button(
            win_row, text="❐ Dock",
            command=lambda: self.engine.control_emulator_window("restore_dock"),
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=ACCENT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=2, sticky="ew", padx=2)

        tk.Button(
            win_row, text="↻ 16:9",
            command=self.engine.force_landscape_tablet_mode,
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=STATUS_OK,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=5, cursor="hand2"
        ).grid(row=0, column=3, sticky="ew", padx=(2, 0))

        tk.Button(
            st_card, text="Re-Apply Tablet/Smartphone Stealth Identity",
            command=lambda: threading.Thread(target=self.engine.apply_live_stealth_smartphone_identity, daemon=True).start(),
            font=(FONT_UI, 8, "bold"), bg=BG_INPUT, fg=STATUS_OK,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=5, cursor="hand2"
        ).pack(fill="x", pady=2)

        tk.Button(
            st_card, text="Open Root Shell Terminal (ADB)",
            command=self.engine.open_root_shell_terminal,
            font=(FONT_UI, 8), bg=BG_INPUT, fg=TEXT_PRIMARY,
            highlightthickness=1, highlightbackground=BORDER_SUBTLE, relief="flat", pady=5, cursor="hand2"
        ).pack(fill="x", pady=2)

        tk.Button(
            st_card, text="Stop Running Emulator",
            command=self.engine.stop_emulator,
            font=(FONT_UI, 8, "bold"), bg="#261216", fg=STATUS_ERR,
            relief="flat", pady=6, cursor="hand2"
        ).pack(fill="x", pady=(6, 0))

    def toggle_sidebar_collapse(self, event=None):
        """
        Toggles the right-hand GAMING EXTEND sidebar between Expanded (340px) and Collapsed Slim-Dock (48px),
        automatically resizing any running Fullscreen Emulator window to claim the extra 292px width!
        """
        self.engine.sidebar_collapsed = not self.engine.sidebar_collapsed
        if self.engine.sidebar_collapsed:
            self.sidebar_expanded_frame.pack_forget()
            self.gaming_sidebar.config(width=SIDEBAR_COLLAPSED_WIDTH)
            self.sidebar_collapsed_frame.pack(fill="both", expand=True)
            self.append_log(f"GAMING EXTEND Sidebar collapsed to Slim-Dock ({SIDEBAR_COLLAPSED_WIDTH}px). Press '⟪' or F10 to expand.", "INFO")
        else:
            self.sidebar_collapsed_frame.pack_forget()
            self.gaming_sidebar.config(width=SIDEBAR_WIDTH)
            self.sidebar_expanded_frame.pack(fill="both", expand=True)
            self.append_log(f"GAMING EXTEND Sidebar expanded ({SIDEBAR_WIDTH}px).", "INFO")

        self.update_idletasks()
        if self.engine.is_emulator_running():
            self.engine.maximize_emulator_window(fullscreen_borderless=False, leave_sidebar=True)

    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================

    def _on_recents_clicked(self):
        self.engine.send_nav_key(187, "APP_SWITCH (RECENTS)")
        self.after(600, self.refresh_background_apps_list)

    def refresh_background_apps_list(self):
        def _worker():
            apps = self.engine.list_running_background_apps()
            def _upd():
                self.bg_apps_listbox.delete(0, "end")
                if not apps:
                    self.bg_apps_listbox.insert("end", "No active background packages")
                else:
                    for a in apps:
                        self.bg_apps_listbox.insert("end", a)
            self.after(0, _upd)
        threading.Thread(target=_worker, daemon=True).start()

    def kill_selected_bg_app(self):
        sel = self.bg_apps_listbox.curselection()
        if not sel:
            return
        pkg = self.bg_apps_listbox.get(sel[0])
        if "." in pkg and " " not in pkg:
            self.engine.kill_background_app(pkg)
            self.after(400, self.refresh_background_apps_list)

    def browse_and_install_apk_or_xapk(self):
        path = filedialog.askopenfilename(
            title="Select APK or XAPK Package to Install",
            filetypes=[
                ("Android Packages (.apk, .xapk, .apkm, .apks)", "*.apk *.xapk *.apkm *.apks"),
                ("APK Files (*.apk)", "*.apk"),
                ("XAPK Bundles (*.xapk)", "*.xapk"),
                ("All Files (*.*)", "*.*")
            ]
        )
        if path:
            self.engine.install_apk_or_xapk(path)

    def pick_and_copy_file_to_emulator(self):
        path = filedialog.askopenfilename(
            title="Select File from PC to Copy to Emulator Shared Folder",
            filetypes=[("All Files (*.*)", "*.*")]
        )
        if path:
            self.engine.sync_shared_folder_to_emulator(specific_file=path)

    def open_keymapper_modal(self):
        KeymapperStudioModal(self, self.engine, on_updated=self._refresh_keymapper_buttons)

    def toggle_keymapper_hotkey(self, event=None):
        self.engine.toggle_keymapper()
        self._refresh_keymapper_buttons()

    def _refresh_keymapper_buttons(self):
        active = self.engine.keymapper_enabled
        fg_c = STATUS_OK if active else ACCENT_PRIMARY
        lbl_top = "⌨ Keymap: ON (F9)" if active else "⌨ Keymapper (F9)"
        lbl_hdr = "⌨ Keymap: ON (F9)" if active else "⌨ Keymap (F9)"
        lbl_sb = "⌨ Keymap: ON (F9)" if active else "⌨ Keymapper (F9)"
        if hasattr(self, "btn_top_keymapper"):
            self.btn_top_keymapper.config(text=lbl_top, fg=fg_c)
        if hasattr(self, "btn_hdr_keymapper"):
            self.btn_hdr_keymapper.config(text=lbl_hdr, fg=fg_c)
        if hasattr(self, "btn_sb_keymapper"):
            self.btn_sb_keymapper.config(text=lbl_sb, fg=fg_c)

    def _on_git_update_clicked(self):
        def _done_cb(ok: bool, msg: str):
            def _notify():
                self.refresh_component_badges()
                if ok:
                    messagebox.showinfo(
                        "Git Repository Update (origin/main)",
                        f"Repository https://github.com/hdi117911-lab/SHOXX_EMU_26.git synchronized:\n\n{msg}"
                    )
                else:
                    messagebox.showwarning(
                        "Git Update Notice",
                        f"Git sync returned a notice:\n\n{msg}"
                    )
            self.after(0, _notify)

        self.engine.git_pull_update(on_done=_done_cb)

    def _setup_native_win32_file_drop(self):
        """
        Hooks native Win32 WM_DROPFILES (DragAcceptFiles) on the ShoXx_Emu studio window
        so users can drag & drop .apk, .xapk, .apkm, .apks, Profile .zip, or any PC file
        directly from Windows Explorer onto the application!
        """
        if os.name != "nt":
            return
        try:
            user32 = ctypes.windll.user32
            shell32 = ctypes.windll.shell32

            GWLP_WNDPROC = -4
            WM_DROPFILES = 0x0233

            WNDPROC = ctypes.WINFUNCTYPE(
                ctypes.c_ssize_t,
                ctypes.c_void_p,
                ctypes.c_uint,
                ctypes.c_size_t,
                ctypes.c_ssize_t
            )

            user32.SetWindowLongPtrW.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
            user32.SetWindowLongPtrW.restype = ctypes.c_void_p
            user32.CallWindowProcW.argtypes = [
                ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t
            ]
            user32.CallWindowProcW.restype = ctypes.c_ssize_t
            shell32.DragAcceptFiles.argtypes = [ctypes.c_void_p, ctypes.c_bool]
            shell32.DragQueryFileW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_wchar_p, ctypes.c_uint]
            shell32.DragQueryFileW.restype = ctypes.c_uint
            shell32.DragFinish.argtypes = [ctypes.c_void_p]

            self._wndproc_refs = []
            self._orig_wndprocs = {}

            inner_hwnd = self.winfo_id()
            top_hwnd = user32.GetParent(inner_hwnd) or inner_hwnd
            target_hwnds = list({h for h in (inner_hwnd, top_hwnd) if h})

            for hwnd in target_hwnds:
                shell32.DragAcceptFiles(hwnd, True)

                def _make_proc(target_h):
                    def _wndproc(h, msg, wparam, lparam):
                        if msg == WM_DROPFILES:
                            hdrop = ctypes.c_void_p(wparam)
                            count = shell32.DragQueryFileW(hdrop, 0xFFFFFFFF, None, 0)
                            dropped = []
                            for idx in range(count):
                                length = shell32.DragQueryFileW(hdrop, idx, None, 0)
                                buf = ctypes.create_unicode_buffer(length + 1)
                                shell32.DragQueryFileW(hdrop, idx, buf, length + 1)
                                dropped.append(buf.value)
                            shell32.DragFinish(hdrop)
                            if dropped:
                                self.after(0, lambda fls=dropped: self.handle_dropped_files(fls))
                            return 0
                        orig = self._orig_wndprocs.get(target_h)
                        if orig:
                            return user32.CallWindowProcW(orig, h, msg, wparam, lparam)
                        return 0
                    return WNDPROC(_wndproc)

                cb = _make_proc(hwnd)
                self._wndproc_refs.append(cb)
                prev = user32.SetWindowLongPtrW(hwnd, GWLP_WNDPROC, ctypes.cast(cb, ctypes.c_void_p).value)
                self._orig_wndprocs[hwnd] = prev
        except Exception as e:
            self.append_log(f"Drag & Drop hook notice: {e}", "WARN")

    def handle_dropped_files(self, file_paths: list):
        """
        Routes dropped files automatically by type:
        - `.apk`, `.xapk`, `.apkm`, `.apks` -> Installs package & OBB onto Emulator
        - `.zip` containing `profile_manifest.json` or `avd_data/` -> Imports Portable Profile
        - Any other file -> Copies into `./Shared_PC_Folder` and syncs to `/sdcard/Download/ShoXx_Shared`
        """
        for path in file_paths:
            if not path or not os.path.exists(path):
                continue
            ext = os.path.splitext(path)[1].lower()
            fname = os.path.basename(path)

            if ext in (".apk", ".xapk", ".apkm", ".apks"):
                self.append_log(f"📦 [DRAG & DROP] Detected Android Package '{fname}' — starting automatic installation...", "CYBER")
                self.engine.install_apk_or_xapk(path)
            elif ext == ".zip":
                is_profile_zip = False
                try:
                    with zipfile.ZipFile(path, "r") as zf:
                        names = zf.namelist()
                        if "profile_manifest.json" in names or any("avd_data/" in n.replace("\\", "/") for n in names):
                            is_profile_zip = True
                except Exception:
                    pass

                if is_profile_zip:
                    self.append_log(f"🔄 [DRAG & DROP] Detected Portable Profile ZIP '{fname}' — importing profile...", "CYBER")
                    try:
                        imp = self.engine.import_profile_zip(path)
                        self._on_profile_switched(imp)
                    except Exception as e:
                        self.append_log(f"Profile ZIP Drop Error: {e}", "ERROR")
                else:
                    self.append_log(f"📂 [DRAG & DROP] Transferring '{fname}' to Shared Folder (/sdcard/Download/ShoXx_Shared)...", "CYBER")
                    self.engine.sync_shared_folder_to_emulator(specific_file=path)
            else:
                self.append_log(f"📂 [DRAG & DROP] Transferring '{fname}' to Shared Folder (/sdcard/Download/ShoXx_Shared)...", "CYBER")
                self.engine.sync_shared_folder_to_emulator(specific_file=path)

    def open_profile_manager_modal(self):
        ProfileManagerModal(self, self.engine, on_profile_selected=self._on_profile_switched)

    def _on_profile_switched(self, prof: dict):
        self.active_prof_lbl.config(text=prof["name"])
        pix = PIXEL_PROFILES.get(prof["pixel_model"], PIXEL_PROFILES["pixel_9_pro_xl"])
        self.active_prof_sub.config(
            text=f"Stealth Identity: {pix['manufacturer']} {pix['model']} ({pix['device']})  •  IMEI: {prof.get('imei')}  •  Carrier: {prof.get('carrier', 'Telekom.de')}"
        )
        self.pixel_var.set(pix["display"])
        self._update_os_button_styles()
        self._update_root_method_styles()
        self._update_launch_button_caption()
        self.append_log(f"Switched Active Profile to '{prof['name']}' (IMEI: {prof.get('imei')})", "CYBER")

    def _download_selected_playstore_rom(self):
        ver = self.engine.selected_android
        st = self.engine.get_rom_status(ver)
        if st["has_playstore"]:
            messagebox.showinfo("Play Store ROM Installed", f"Android {ver} Google Play Store ROM is already installed in ./sdk/!")
            return
        self.engine.download_playstore_rom(ver, on_done=lambda ok: self.after(0, self.refresh_component_badges))

    def select_android_version(self, ver_key: str):
        self.engine.selected_android = ver_key
        self.engine.sync_current_settings_to_active_profile()
        v_info = ANDROID_VERSIONS[ver_key]
        self._update_os_button_styles()
        self._update_launch_button_caption()
        self.append_log(f"Selected Android OS Target: {v_info['name']}", "CYBER")

    def _update_os_button_styles(self):
        for k, btn in self.os_buttons.items():
            if k == self.engine.selected_android:
                btn.config(bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY, highlightthickness=1, highlightbackground=BORDER_FOCUS)
            else:
                btn.config(bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=1, highlightbackground=BORDER_SUBTLE)

    def select_root_method(self, rm_key: str):
        self.engine.root_method = rm_key
        self.engine.sync_current_settings_to_active_profile()
        m_info = ROOT_METHODS[rm_key]
        self._update_root_method_styles()
        self._update_launch_button_caption()
        self.append_log(f"Selected Root Architecture: {m_info['name']}", "ROOT")

        if self.engine.is_emulator_running() and self.engine.root_enabled:
            threading.Thread(target=self.engine.apply_live_root_state, args=(True, rm_key), daemon=True).start()

    def _update_root_method_styles(self):
        m_short = ROOT_METHODS[self.engine.root_method]["short"]
        if self.engine.root_enabled:
            self.root_status_lbl.config(text=f"SUPERUSER ROOT ACCESS: ENABLED ({m_short})", fg=STATUS_OK)
            self.root_toggle_btn.config(text="Root: ON", bg=STATUS_OK, fg=BG_ROOT)
        else:
            self.root_status_lbl.config(text="SUPERUSER ROOT ACCESS: DISABLED (Unrooted Stealth)", fg=TEXT_SECONDARY)
            self.root_toggle_btn.config(text="Root: OFF", bg=BG_CARD, fg=TEXT_SECONDARY)

        for k, btn in self.rm_buttons.items():
            if k == self.engine.root_method:
                btn.config(bg=ACCENT_PRIMARY, fg=TEXT_PRIMARY, highlightthickness=1, highlightbackground=BORDER_FOCUS)
            else:
                btn.config(bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=1, highlightbackground=BORDER_SUBTLE)

    def _update_launch_button_caption(self):
        pix_model = PIXEL_PROFILES[self.engine.selected_pixel]["model"]
        root_tag = ROOT_METHODS[self.engine.root_method]["short"] if self.engine.root_enabled else "Unrooted"
        rom_st = self.engine.get_rom_status(self.engine.selected_android)
        play_tag = "Play Store" if rom_st["has_playstore"] else "Base ROM"
        self.btn_launch.config(
            text=f"Launch {pix_model} in Fullscreen  (Android {self.engine.selected_android} • {play_tag} • {root_tag})"
        )
        self.tele_lbl.config(
            text=f"Device: {pix_model}  •  OS: Android {self.engine.selected_android} ({play_tag})  •  Root: {root_tag}"
        )

    def toggle_root_access(self):
        new_state = not self.engine.root_enabled
        self.engine.root_enabled = new_state
        self.engine.sync_current_settings_to_active_profile()
        self._update_root_method_styles()
        self._update_launch_button_caption()

        if new_state:
            self.append_log(f"Root Access enabled: {ROOT_METHODS[self.engine.root_method]['name']}", "ROOT")
        else:
            self.append_log("Root Access disabled: Unrooted Retail Smartphone Stealth active.", "WARN")

        if self.engine.is_emulator_running():
            threading.Thread(target=self.engine.apply_live_root_state, args=(new_state, self.engine.root_method), daemon=True).start()

    def apply_optimal_settings_clicked(self):
        self.sys_report = self.engine.analyze_system_hardware()
        opt = self.engine.apply_optimal_settings_to_engine()
        self.pixel_var.set(PIXEL_PROFILES[opt["pixel_profile"]]["display"])
        self.ram_var.set(opt["ram_label"])
        self.cores_var.set(opt["cores_label"])
        self._update_launch_button_caption()

    def _on_hw_changed(self, *args):
        pix_s = self.pixel_var.get()
        for pk, pv in PIXEL_PROFILES.items():
            if pv["display"] == pix_s:
                self.engine.selected_pixel = pk
                break

        ram_s = self.ram_var.get()
        self.engine.ram_mb = int(ram_s.split()[0])

        cores_s = self.cores_var.get()
        self.engine.cores = int(cores_s.split()[0])

        self.engine.sync_current_settings_to_active_profile()
        self._update_launch_button_caption()

    def refresh_component_badges(self):
        self.plugins_list = self.engine.inspect_plugins_and_tools()
        self._update_launch_button_caption()

    def start_one_click_setup(self, auto_launch_after: bool = False):
        if self.is_busy:
            self.append_log("Setup task is already running — please wait...", "WARN")
            return
        self.is_busy = True
        self._on_hw_changed()

        def _worker():
            ok = self.engine.run_one_click_auto_setup(target_android=self.engine.selected_android, setup_all_versions=False)
            self.after(0, self.refresh_component_badges)
            self.is_busy = False
            if ok and auto_launch_after:
                self.after(300, self.start_emulator_launch)

        threading.Thread(target=_worker, daemon=True).start()

    def show_emulator_viewport_frame(self):
        """Switches the main left workspace to the Embedded Studio Emulator Container Frame."""
        if not self.showing_emulator_frame:
            self.dashboard_body.pack_forget()
            self.emulator_viewport_frame.pack(fill="both", expand=True, padx=14, pady=10)
            self.showing_emulator_frame = True
        self.btn_toggle_view.config(text="⊞ Studio Dashboard", fg=ACCENT_PRIMARY)
        pix_m = PIXEL_PROFILES[self.engine.selected_pixel]["model"]
        r_tag = ROOT_METHODS[self.engine.root_method]["short"] if self.engine.root_enabled else "Unrooted"
        self.emu_frame_title_lbl.config(
            text=f"●  ANDROID EMULATOR STUDIO FRAME — {pix_m} (Landscape 16:9 • Android {self.engine.selected_android} • {r_tag})"
        )
        self.update_idletasks()
        cw = max(640, self.emu_host_container.winfo_width())
        ch = max(400, self.emu_host_container.winfo_height())
        self.engine.embed_container_hwnd = self.emu_host_container.winfo_id()
        self.engine.embed_container_size = (cw, ch)
        if self.engine.is_emulator_running() and self.engine.embed_mode_enabled:
            self.engine.embed_emulator_in_container(self.engine.embed_container_hwnd, cw, ch)

    def show_studio_dashboard(self):
        """Switches the main left workspace back to the 2-Column Studio Configuration & Telemetry Dashboard."""
        if self.showing_emulator_frame:
            self.emulator_viewport_frame.pack_forget()
            self.dashboard_body.pack(fill="both", expand=True, padx=20, pady=16)
            self.showing_emulator_frame = False
        self.btn_toggle_view.config(text="⊞ Emulator Frame", fg=STATUS_OK)

    def toggle_studio_viewport_mode(self):
        if self.showing_emulator_frame:
            self.show_studio_dashboard()
        else:
            self.show_emulator_viewport_frame()

    def toggle_embed_or_undock(self):
        """Toggles between embedding the Emulator inside the Studio Frame (`SetParent`) and a Floating Framed Window."""
        if self.engine.embed_mode_enabled:
            self.engine.undock_emulator_window()
            self.btn_undock_embed.config(text="⊞ Embed in Frame", fg=STATUS_OK)
        else:
            self.engine.embed_mode_enabled = True
            self.show_emulator_viewport_frame()
            self.btn_undock_embed.config(text="❐ Undock Window", fg=ACCENT_PRIMARY)

    def _minimize_emulator_or_studio(self):
        if not self.engine.embed_mode_enabled and self.engine.is_emulator_running():
            self.engine.control_emulator_window("minimize")
        else:
            self.iconify()

    def _stop_and_return_to_dashboard(self):
        self.engine.stop_emulator()
        self.show_studio_dashboard()

    def _on_emu_container_resized(self, event=None):
        cw = max(640, self.emu_host_container.winfo_width())
        ch = max(400, self.emu_host_container.winfo_height())
        self.engine.embed_container_hwnd = self.emu_host_container.winfo_id()
        self.engine.embed_container_size = (cw, ch)
        if self.engine.is_emulator_running() and self.engine.embed_mode_enabled:
            self.engine.embed_emulator_in_container(self.engine.embed_container_hwnd, cw, ch)

    def start_emulator_launch(self):
        self._on_hw_changed()
        self.show_emulator_viewport_frame()
        self.progress_pct = 35
        pix_m = PIXEL_PROFILES[self.engine.selected_pixel]["model"]
        self.progress_status = f"Launching {pix_m} (Android {self.engine.selected_android}) inside Embedded Studio Frame..."
        threading.Thread(
            target=self.engine.launch_emulator,
            args=(self._on_emulator_booted,),
            daemon=True
        ).start()

    def _on_emulator_booted(self):
        m_short = ROOT_METHODS[self.engine.root_method]["short"] if self.engine.root_enabled else "Unrooted Stealth"
        self.update_progress_threadsafe(100, f"Active: {PIXEL_PROFILES[self.engine.selected_pixel]['model']} Running in Fullscreen ({m_short})")
        info = self.engine.verify_device_info()
        if info["connected"]:
            ps_txt = "Play Store Active" if info["playstore"] else "Base ROM"
            self.after(0, lambda: self.tele_lbl.config(
                text=f"LIVE: {info['model']} ({info['device']} / {info['tags']})  •  Android {info['release']}  •  {ps_txt}  •  {m_short}",
                fg=STATUS_OK
            ))
            self.after(500, self.refresh_background_apps_list)

    def append_log_threadsafe(self, msg: str, level: str = "INFO"):
        try:
            self.after(0, lambda: self.append_log(msg, level))
        except Exception:
            pass

    def append_log(self, msg: str, level: str = "INFO"):
        try:
            ts = time.strftime("%H:%M:%S")
            self.log_text.insert("end", f"[{ts}] {msg}\n", level)
            self.log_text.see("end")
        except Exception:
            pass

    def update_progress_threadsafe(self, pct: float, status: str = ""):
        def _upd():
            self.progress_pct = max(0.0, min(100.0, float(pct)))
            if status:
                self.progress_status = status
            self.refresh_component_badges()
        try:
            self.after(0, _upd)
        except Exception:
            pass

    def _draw_mini_gauge(self, canvas, cx, cy, r, pct, color, title, sub):
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline=BORDER_SUBTLE, width=5)
        ext = -int(300 * (max(0.0, min(100.0, pct)) / 100.0))
        canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=240, extent=ext, style="arc", outline=color, width=5)
        canvas.create_text(cx, cy - 1, text=f"{int(pct)}%", font=(FONT_UI, 10, "bold"), fill=TEXT_PRIMARY)
        canvas.create_text(cx, cy + r + 14, text=title, font=(FONT_UI, 8, "bold"), fill=TEXT_PRIMARY)
        canvas.create_text(cx, cy + r + 27, text=sub, font=(FONT_UI, 7), fill=TEXT_MUTED)

    def _animate_dashboard(self):
        self.anim_tick += 1.0

        if int(self.anim_tick) % 90 == 0:
            self.sys_report = self.engine.analyze_system_hardware()
            self.plugins_list = self.engine.inspect_plugins_and_tools()

        # 1. Left Column: Clean Module Readiness Table
        pc = self.plugins_canvas
        pc.delete("all")
        pw = pc.winfo_width() or 520
        ph = pc.winfo_height() or 195

        num_p = len(self.plugins_list)
        row_h = max(22, (ph - 8) // max(1, num_p))

        for idx, plug in enumerate(self.plugins_list):
            ry = 4 + idx * row_h
            ry2 = ry + row_h - 2
            is_inst = plug["installed"]

            if idx % 2 == 0:
                pc.create_rectangle(4, ry, pw - 4, ry2, fill=BG_INPUT, outline="")

            dot_c = STATUS_OK if is_inst else STATUS_WARN
            pc.create_oval(14, (ry + ry2) // 2 - 3, 20, (ry + ry2) // 2 + 3, fill=dot_c, outline="")
            pc.create_text(30, (ry + ry2) // 2, text=plug["name"], font=(FONT_UI, 8, "bold"), fill=TEXT_PRIMARY, anchor="w")
            pc.create_text(pw - 12, (ry + ry2) // 2, text=plug["status_text"], font=(FONT_MONO, 8), fill=dot_c, anchor="e")

        # 2. Right Column: Clean System Telemetry & Optimal Settings Card
        sc = self.sys_canvas
        sc.delete("all")
        sw_c = sc.winfo_width() or 520
        sh_c = sc.winfo_height() or 225
        sr = self.sys_report
        opt = sr["optimal"]

        gw = sw_c // 4
        gy = 44
        self._draw_mini_gauge(sc, gw * 0 + gw // 2, gy, 27, sr["cpu_score_pct"], ACCENT_PRIMARY, "CPU", f"{sr['cpu_threads']} Cores")
        self._draw_mini_gauge(sc, gw * 1 + gw // 2, gy, 27, 100 - sr["ram_load_pct"], STATUS_OK, "RAM Free", f"{sr['ram_avail_mb']} MB")
        self._draw_mini_gauge(sc, gw * 2 + gw // 2, gy, 27, sr["gpu_score_pct"], ACCENT_PRIMARY, "GPU VRAM", f"{sr['primary_gpu']['vram_mb']} MB")
        self._draw_mini_gauge(sc, gw * 3 + gw // 2, gy, 27, opt["score"], STATUS_OK, "Performance", f"{opt['score']}/100")

        ty = 104
        hw_rows = [
            ("Processor", f"{sr['cpu_name']} ({sr['cpu_threads']} Threads @ {sr['cpu_mhz']} MHz)"),
            ("Graphics", f"{sr['primary_gpu']['name']} ({sr['primary_gpu']['vram_mb']} MB VRAM)  •  {sr['accel_detail']}"),
            ("Recommended", f"{opt['cores']} Cores  •  {opt['ram_mb']} MB RAM  •  GPU '{opt['gpu_mode']}'  •  Retail Stealth Active"),
        ]
        for r_i, (tag, val) in enumerate(hw_rows):
            ry = ty + r_i * 36
            sc.create_rectangle(10, ry, sw_c - 10, ry + 30, fill=BG_INPUT, outline=BORDER_SUBTLE, width=1)
            sc.create_text(20, ry + 15, text=tag, font=(FONT_UI, 8, "bold"), fill=TEXT_SECONDARY, anchor="w")
            sc.create_text(110, ry + 15, text=val[:64], font=(FONT_UI, 8), fill=TEXT_PRIMARY, anchor="w")

        # 3. Bottom Subtle Status & Progress Footer
        fc = self.footer_canvas
        fc.delete("all")
        fw = fc.winfo_width() or (self.sw - SIDEBAR_WIDTH)

        fc.create_line(0, 0, fw, 0, fill=BORDER_SUBTLE, width=1)
        fc.create_text(
            20, 14,
            text=self.progress_status,
            font=(FONT_UI, 8), fill=TEXT_SECONDARY, anchor="w"
        )
        fc.create_text(
            fw - 20, 14,
            text=f"Portable Root: {BASE_DIR}   •   {int(self.progress_pct)}%",
            font=(FONT_MONO, 8), fill=TEXT_MUTED, anchor="e"
        )

        # Slim 3px progress bar at the very bottom edge
        fill_w = int(fw * (self.progress_pct / 100.0))
        fc.create_rectangle(0, 34, fw, 38, fill=BG_INPUT, outline="")
        if fill_w > 0:
            bar_c = STATUS_OK if self.progress_pct >= 100 else ACCENT_PRIMARY
            fc.create_rectangle(0, 34, fill_w, 38, fill=bar_c, outline="")

        self.after(60, self._animate_dashboard)

    def _replay_splash(self):
        self.splash = ExecutiveSplashOverlay(self, self.engine, on_complete=None)

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    auto_boot = "--auto-boot" in sys.argv
    app = ShoXxApp(auto_boot=auto_boot)
    app.mainloop()
