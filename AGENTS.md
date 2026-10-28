# 🤖 AGENTS.md — ShoXx_Emu Project Rules & Optimization Workflow

## 1. Mandatory Post-Step Optimization Proposals (Approval Required)
- **Nach jedem abgeschlossenen Arbeitsschritt** MUSS der Agent am Ende seiner Antwort **konkrete, technisch fundierte Optimierungsvorschläge** (Performance, Anti-Detect/Stealth, Gaming-Features, UI/UX oder Architektur) für das Projekt **ShoXx_Emu** unterbreiten.
- **WICHTIG (Strikte Genehmigungspflicht)**: Diese vorgeschlagenen Optimierungen dürfen **NIEMALS eigenmächtig sofort umgesetzt** werden. Sie müssen immer zuerst dem Nutzer präsentiert und **explizit durch den Nutzer genehmigt** werden, bevor sie im nächsten Schritt implementiert werden.

## 2. Core Architecture & Requirements of ShoXx_Emu
0. **100% Strikte Portabilität im Hauptordner (`BASE_DIR`) für Weitergabe an andere User & PCs**:
   - **Alle** Ausführungen, temporären Dateien, Downloads, SDK-Pakete, System-Images, AVD-Container, Snapshots, ADB-Keys und Logs müssen **ausschließlich innerhalb des Programm-Hauptordners** (`./sdk`, `./avd_data`, `./downloads`, `./_cache`, `./Shared_PC_Folder`, `./python_portable`, `./root_methods`) stattfinden.
   - Es dürfen **keine** Dateien in `C:\Users\<User>\.android`, `%LOCALAPPDATA%` oder `%TEMP%` des Host-PCs geschrieben oder von dort vorausgesetzt werden (`TEMP`/`TMP`/`USERPROFILE`/`ANDROID_PREFS_ROOT`/`ANDROID_SDK_HOME` werden strikt auf den Programm-Hauptordner isoliert).
   - Beim Start auf einem anderen PC oder Laufwerk führt `ShoXx_Emu` automatisch ein **Dynamic Path Relinking** aller `.ini`- und `.conf`-Dateien auf den aktuellen Programmordner durch, sodass der komplette Ordner per USB-Stick/ZIP auf jedem beliebigen PC sofort lauffähig ist.
1. **100% Anti-Emulator-Detection (Real Smartphone Stealth Identity)**:
   - Der Emulator darf von Apps, Spielen und Anti-Cheat-/SafetyNet-/Play-Integrity-Prüfungen **nicht als Emulator (`generic`, `sdk_gphone`, `qemu`, `goldfish`, `ranchu`) erkannt** werden.
   - Stattdessen wird ein echtes Retail-Smartphone (**Google Pixel 9 Pro XL / `komodo`**, **Pixel 9 Pro / `caiman`**, **Pixel 9 Pro Fold / `comet`**) mit verifiziertem Google-Release-Fingerprint (`release-keys`, `user`), realistischer IMEI/MEID, Mobilfunk-Betreiber (`T-Mobile / Telekom.de`), Batterie-Simulation, Sensoren, versteckten QEMU-Pipes/Dateien und System-Property-Spoofing (`resetprop` / `setprop` + `build.prop` Patching) emuliert.
2. **Alle ROMs (Android 15, 16, 17) mit offiziellem Google Play Store (`google_apis_playstore`)**:
   - Sämtliche angebotenen ROMs (Android 15 API 35, Android 16 API 36, Android 17 API 37) nutzen die offiziellen `google_apis_playstore` System-Images inklusive vorinstalliertem **Google Play Store (`com.android.vending`)** und **Google Play Services (`com.google.android.gms`)** (`PlayStore.enabled = yes`).
   - Basis-Dateien zur sofortigen Nutzung des Emulators sind lokal integriert; zusätzliche Play-Store-ROMs können direkt im Emulator-Manager per One-Click heruntergeladen werden.
3. **APK & XAPK Installer mit Dateidialog**:
   - Unterstützt sowohl klassische `.apk` als auch komplexe `.xapk` / `.apkm` / `.apks` Pakete (automatisches Entpacken von Split-APKs via `adb install-multiple` + automatischer Push von `.obb`-Spieldaten nach `/sdcard/Android/obb/<package>/`).
4. **Vollbild-Oberfläche mit fixiertem rechtem GAMING EXTEND Seitenpanel**:
   - Im Vollbildmodus wird der Android-Emulator exakt auf den linken Hauptbereich (`ScreenW - SidebarW`) gedockt, während auf der **rechten Seite ein fixiertes Neon-"GAMING EXTEND"-Panel** permanent sichtbar bleibt.
   - Das rechte Panel enthält:
     - **Android-Navigationsbuttons**: `◀ ZURÜCK (Back)`, `⏺ HOME`, `▣ APPS (Recents / Hintergrund laufende Apps)` + Live-Task-Manager zum Anzeigen/Beenden laufender Hintergrund-Apps.
     - **Shared Folder (PC ↔ Emulator)**: Direkter Datei-Transfer-Manager für den gemeinsamen Ordner `d:\SHOXX_EMU_26\Shared_PC_Folder` ↔ `/sdcard/Download/ShoXx_Shared` (inkl. Datei-Upload, Pull und Ordner-Öffnen).
     - **Gaming Extend Controls**: Anti-Detect Stealth-Status, FPS/Performance-Boost, APK/XAPK-Schnellinstallation, Root-Live-Switch, Lautstärke, Screenshot & Vollbild-Docking.
5. **Multi-Profil-Manager (Untermenü beim Start & im Dashboard)**:
   - Erlaubt das Anlegen, Klonen, Bearbeiten, Löschen und Auswählen mehrerer unabhängiger Emulator-Profile (eigene Android-Version 15/16/17, eigenes Pixel-Modell, eigene IMEI/Android-ID, eigene RAM/CPU-Werte, eigene Root-Methode: 1. Magisk, 2. KernelSU, 3. APatch + Native SU).
