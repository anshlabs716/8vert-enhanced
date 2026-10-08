#!/usr/bin/env python3
"""
enhanced.py - All-in-One Calculator & Converter
Liquid Glass theme · WM Wobble · Fullscreen · Fast typing
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import math
import re
import json
import os
from datetime import datetime

# =============================================================================
# CONFIG
# =============================================================================
CONFIG_DIR = os.path.expanduser("~/.enhanced")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
HISTORY_FILE = os.path.join(CONFIG_DIR, "history.txt")

# =============================================================================
# LIQUID GLASS THEME
# =============================================================================
COLORS = {
    "bg":      "#0a0a0f",
    "bg2":     "#12121e",
    "bg3":     "#1a1a2e",
    "bg4":     "#2a2a4a",
    "glass":   "#1a1a2e",
    "glass2":  "#222244",
    "fg":      "#e8e8f0",
    "fg2":     "#a0a0b8",
    "fg3":     "#606080",
    "accent":  "#6c63ff",
    "accent2": "#5a52d5",
    "accent3": "#8a82ff",
    "green":   "#4ade80",
    "orange":  "#fbbf24",
    "red":     "#f87171",
    "purple":  "#a78bfa",
    "pink":    "#f472b6",
    "cyan":    "#22d3ee",
    "border":  "#2a2a4a",
}

# =============================================================================
# CONVERTER DATA
# =============================================================================
CONVERTERS = {
    "Length": {
        "units": ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"],
        "base":  {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0,
                  "in": 0.0254, "ft": 0.3048, "yd": 0.9144, "mi": 1609.344}
    },
    "Mass": {
        "units": ["mg", "g", "kg", "t", "oz", "lb", "st"],
        "base":  {"mg": 0.001, "g": 1.0, "kg": 1000.0, "t": 1000000.0,
                  "oz": 28.3495, "lb": 453.592, "st": 6350.293}
    },
    "Temperature": {"units": ["°C", "°F", "K"], "special": "temp"},
    "Area": {
        "units": ["mm²", "cm²", "m²", "km²", "in²", "ft²", "yd²", "mi²", "ha", "ac"],
        "base":  {"mm²": 1e-6, "cm²": 0.0001, "m²": 1.0, "km²": 1e6,
                  "in²": 0.00064516, "ft²": 0.092903, "yd²": 0.836127,
                  "mi²": 2589988.11, "ha": 10000.0, "ac": 4046.85642}
    },
    "Volume": {
        "units": ["ml", "L", "m³", "tsp", "tbsp", "fl oz", "cup", "pt", "qt", "gal"],
        "base":  {"ml": 0.001, "L": 1.0, "m³": 1000.0, "tsp": 0.00492892,
                  "tbsp": 0.0147868, "fl oz": 0.0295735, "cup": 0.236588,
                  "pt": 0.473176, "qt": 0.946353, "gal": 3.78541}
    },
    "Speed": {
        "units": ["m/s", "km/h", "mph", "kn", "ft/s"],
        "base":  {"m/s": 1.0, "km/h": 0.277778, "mph": 0.44704,
                  "kn": 0.514444, "ft/s": 0.3048}
    },
    "Time": {
        "units": ["ms", "s", "min", "h", "day", "week", "month", "year"],
        "base":  {"ms": 0.001, "s": 1.0, "min": 60.0, "h": 3600.0,
                  "day": 86400.0, "week": 604800.0, "month": 2629800.0,
                  "year": 31557600.0}
    },
    "Digital": {
        "units": ["b", "B", "KB", "MB", "GB", "TB", "PB"],
        "base":  {"b": 0.125, "B": 1.0, "KB": 1024.0, "MB": 1048576.0,
                  "GB": 1073741824.0, "TB": 1099511627776.0,
                  "PB": 1125899906842624.0}
    },
    "Energy": {
        "units": ["J", "kJ", "cal", "kcal", "Wh", "kWh", "eV", "BTU"],
        "base":  {"J": 1.0, "kJ": 1000.0, "cal": 4.184, "kcal": 4184.0,
                  "Wh": 3600.0, "kWh": 3600000.0, "eV": 1.602176634e-19,
                  "BTU": 1055.05585}
    },
    "Pressure": {
        "units": ["Pa", "kPa", "bar", "psi", "atm", "Torr"],
        "base":  {"Pa": 1.0, "kPa": 1000.0, "bar": 100000.0,
                  "psi": 6894.757, "atm": 101325.0, "Torr": 133.322}
    },
    "Angle": {
        "units": ["deg", "rad", "grad", "arcmin", "arcsec"],
        "base":  {"deg": 0.0174533, "rad": 1.0, "grad": 0.015708,
                  "arcmin": 0.000290888, "arcsec": 0.00000484814}
    }
}

# =============================================================================
# MAIN APP
# =============================================================================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced")
        self.root.geometry("1200x850")
        self.root.minsize(1050, 750)
        self.root.configure(bg=COLORS["bg"])
        # No overrideredirect — keep the WM managing the window so focus,
        # minimize and keyboard all work correctly out of the box.
        self.root.overrideredirect(False)

        # Config
        self.config = self._load_config()
        self.notes_format     = self.config.get("notes_format", "md")
        self.auto_save_enabled = self.config.get("auto_save", True)
        self.cursor_blink     = self.config.get("cursor_blink", True)
        self.wobble_enabled   = self.config.get("wobble", True)

        # State
        self.history        = self._load_history()
        self.calc_history   = []
        self._cursor_job    = None
        self._cursor_on     = True
        self._wobble_job    = None
        self._glass_job     = None
        self._glass_angle   = 0.0
        self.is_fullscreen  = False
        self._pre_fs_geometry = "1200x850"
        self._wobble_orig_x = 0
        self._wobble_orig_y = 0
        self._wobble_vx     = 0.0
        self._wobble_vy     = 0.0

        # Build
        self._build_ui()
        self._load_notes()
        self._update_history_list()

        # Start cursor blink (only in notes widget — not on every click)
        if self.cursor_blink:
            self._start_cursor_blink()

        # Glass shimmer — slower tick so it doesn't choke the event loop
        self._animate_glass()

        # Autosave
        if self.auto_save_enabled:
            self._auto_save()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<Control-s>", lambda e: self._save_notes())
        self.root.bind("<Control-q>", lambda e: self._on_close())
        self.root.bind("<Escape>",    self._on_escape)
        self.root.bind("<Control-o>", lambda e: self._toggle_options())

        # Drag
        self._drag = {"x": 0, "y": 0}
        self.title_bar.bind("<Button-1>",  self._drag_start)
        self.title_bar.bind("<B1-Motion>", self._drag_move)
        # Wobble only on title bar double-click — not every widget click
        self.title_bar.bind("<Double-Button-1>", self._trigger_wobble)

    def _on_escape(self, event=None):
        if self.is_fullscreen:
            self._toggle_fullscreen()
        else:
            self.entry.focus_set()

    # =========================================================================
    # WINDOW DRAG
    # =========================================================================
    def _drag_start(self, event):
        if event.widget in (self._btn_fs, self._btn_close, self._btn_min):
            return
        self._drag["x"] = event.x
        self._drag["y"] = event.y

    def _drag_move(self, event):
        if event.widget in (self._btn_fs, self._btn_close, self._btn_min):
            return
        x = self.root.winfo_x() + event.x - self._drag["x"]
        y = self.root.winfo_y() + event.y - self._drag["y"]
        self.root.geometry(f"+{x}+{y}")

    # =========================================================================
    # WM WOBBLE — only triggered explicitly, not on every click
    # =========================================================================
    def _trigger_wobble(self, event=None):
        if not self.wobble_enabled or self.is_fullscreen:
            return
        if self._wobble_job:
            self.root.after_cancel(self._wobble_job)
            self._wobble_job = None
        self._wobble_orig_x = self.root.winfo_x()
        self._wobble_orig_y = self.root.winfo_y()
        self._wobble_vx = 14.0
        self._wobble_vy = -4.0
        self._do_wobble()

    def _do_wobble(self):
        damping = 0.82
        self._wobble_vx *= damping
        self._wobble_vy *= damping
        if abs(self._wobble_vx) > 0.3 or abs(self._wobble_vy) > 0.3:
            nx = self._wobble_orig_x + int(self._wobble_vx)
            ny = self._wobble_orig_y + int(self._wobble_vy * 0.4)
            try:
                self.root.geometry(f"+{nx}+{ny}")
            except Exception:
                pass
            self._wobble_job = self.root.after(20, self._do_wobble)
        else:
            self._wobble_job = None
            try:
                self.root.geometry(f"+{self._wobble_orig_x}+{self._wobble_orig_y}")
            except Exception:
                pass

    # =========================================================================
    # FULLSCREEN
    # =========================================================================
    def _toggle_fullscreen(self):
        if self.is_fullscreen:
            self.root.geometry(self._pre_fs_geometry)
            self.is_fullscreen = False
            self._btn_fs.config(text="⛶")
            self._set_status("Windowed mode", COLORS["fg2"])
        else:
            self._pre_fs_geometry = self.root.geometry()
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{sw}x{sh}+0+0")
            self.is_fullscreen = True
            self._btn_fs.config(text="❐")
            self._set_status("Fullscreen mode", COLORS["accent"])
        self.root.focus_force()

    def _minimize(self):
        self.root.iconify()

    # =========================================================================
    # GLASS SHIMMER — 250ms tick; purely cosmetic, won't block typing
    # =========================================================================
    def _animate_glass(self):
        r = 20 + int(6 * math.sin(self._glass_angle + 0.5))
        g = 20 + int(6 * math.sin(self._glass_angle + 1.5))
        b = 40 + int(8 * math.sin(self._glass_angle + 2.5))
        color = f"#{r:02x}{g:02x}{b:02x}"
        try:
            self.glass_frame.configure(bg=color)
        except Exception:
            pass
        self._glass_angle += 0.05
        self._glass_job = self.root.after(250, self._animate_glass)

    # =========================================================================
    # CURSOR BLINK — steady 500ms toggle, never restarted mid-typing
    # =========================================================================
    def _start_cursor_blink(self):
        if self._cursor_job:
            self.root.after_cancel(self._cursor_job)
        self._cursor_on = True
        self._tick_cursor()

    def _stop_cursor_blink(self):
        if self._cursor_job:
            self.root.after_cancel(self._cursor_job)
            self._cursor_job = None
        try:
            self.notes.configure(insertbackground=COLORS["accent"])
            self._cursor_ind.config(fg=COLORS["accent"])
        except Exception:
            pass

    def _tick_cursor(self):
        self._cursor_on = not self._cursor_on
        color = COLORS["accent"] if self._cursor_on else COLORS["bg"]
        ind_color = COLORS["accent"] if self._cursor_on else COLORS["fg3"]
        try:
            self.notes.configure(insertbackground=color)
            self._cursor_ind.config(fg=ind_color)
        except Exception:
            pass
        # Also blink the entry and calc display so cursor is visible everywhere
        try:
            self.entry.configure(insertbackground=color)
            self._calc_disp.configure(insertbackground=color)
            self._val_entry.configure(insertbackground=color)
        except Exception:
            pass
        self._cursor_job = self.root.after(530, self._tick_cursor)

    # =========================================================================
    # CONFIG / DATA
    # =========================================================================
    def _load_config(self):
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            return {"notes_format": "md", "auto_save": True, "cursor_blink": True, "wobble": True}

    def _save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f)
        except Exception:
            pass

    def _load_history(self):
        try:
            with open(HISTORY_FILE) as f:
                return [l.strip() for l in f if l.strip()]
        except Exception:
            return []

    def _save_history(self):
        try:
            with open(HISTORY_FILE, "w") as f:
                f.write("\n".join(self.history))
        except Exception:
            pass

    def _notes_path(self):
        ext = "md" if self.notes_format == "md" else "txt"
        return os.path.join(CONFIG_DIR, f"notes.{ext}")

    def _load_notes(self):
        try:
            with open(self._notes_path()) as f:
                self.notes.delete(1.0, tk.END)
                self.notes.insert(1.0, f.read())
        except Exception:
            pass

    def _save_notes(self):
        try:
            with open(self._notes_path(), "w") as f:
                f.write(self.notes.get(1.0, tk.END))
            self._set_status("💾 Saved ✓", COLORS["green"])
        except Exception:
            self._set_status("❌ Save failed", COLORS["red"])

    def _set_status(self, text, color=None, duration=1500):
        self.status.config(text=text, fg=color or COLORS["fg2"])
        if duration:
            self.root.after(duration, lambda: self.status.config(text="Ready", fg=COLORS["fg2"]))

    # =========================================================================
    # AUTO SAVE
    # =========================================================================
    def _auto_save(self):
        if self.auto_save_enabled:
            self._save_notes()
            self._save_history()
        self.root.after(30000, self._auto_save)

    # =========================================================================
    # BUILD UI
    # =========================================================================
    def _build_ui(self):
        self.main = tk.Frame(self.root, bg=COLORS["bg"])
        self.main.pack(fill=tk.BOTH, expand=True)

        self._build_title_bar()

        content = tk.Frame(self.main, bg=COLORS["bg2"])
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.glass_frame = tk.Frame(content, bg=COLORS["glass"])
        self.glass_frame.pack(fill=tk.BOTH, expand=True)

        self._build_entry(self.glass_frame)

        self.notebook = ttk.Notebook(self.glass_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self._build_converter()
        self._build_calculator()
        self._build_notes_tab()
        self._build_history_tab()
        self._build_options_tab()

        self._build_status_bar()
        self._apply_styles()

    def _apply_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TNotebook", background=COLORS["bg2"], borderwidth=0)
        s.configure("TNotebook.Tab",
                    background=COLORS["bg3"], foreground=COLORS["fg2"],
                    padding=[25, 14], font=("Segoe UI", 11),
                    borderwidth=0, focuscolor="none")
        s.map("TNotebook.Tab",
              background=[("selected", COLORS["accent2"])],
              foreground=[("selected", "white")])
        s.configure("TCombobox",
                    fieldbackground=COLORS["bg"], background=COLORS["bg3"],
                    foreground=COLORS["fg"], arrowcolor=COLORS["fg2"], borderwidth=0)
        s.map("TCombobox", fieldbackground=[("readonly", COLORS["bg"])])
        s.configure("TButton",
                    background=COLORS["bg3"], foreground=COLORS["fg"],
                    borderwidth=0, focuscolor="none", padding=[15, 8])
        s.map("TButton", background=[("active", COLORS["bg4"])])

    # =========================================================================
    # TITLE BAR
    # =========================================================================
    def _build_title_bar(self):
        self.title_bar = tk.Frame(self.main, bg=COLORS["bg2"], height=45)
        self.title_bar.pack(fill=tk.X, pady=(0, 5))
        self.title_bar.pack_propagate(False)

        tk.Label(self.title_bar, text="✦ Enhanced", font=("Segoe UI", 18, "bold"),
                 bg=COLORS["bg2"], fg=COLORS["accent"]).pack(side=tk.LEFT, padx=20)

        ctrl = tk.Frame(self.title_bar, bg=COLORS["bg2"])
        ctrl.pack(side=tk.RIGHT, padx=10)

        # Notes format buttons
        fmt_f = tk.Frame(ctrl, bg=COLORS["bg2"])
        fmt_f.pack(side=tk.LEFT, padx=10)
        tk.Label(fmt_f, text="Notes:", bg=COLORS["bg2"],
                 fg=COLORS["fg2"], font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 8))
        self._fmt_btns = []
        for fmt in ["MD", "TXT"]:
            active = fmt.lower() == self.notes_format
            btn = tk.Button(fmt_f, text=fmt, font=("Segoe UI", 10, "bold"),
                            bg=COLORS["accent2"] if active else COLORS["bg3"],
                            fg="white" if active else COLORS["fg2"],
                            relief=tk.FLAT, cursor="hand2", padx=10, pady=3,
                            command=lambda f=fmt: self._change_format(f))
            btn.pack(side=tk.LEFT, padx=2)
            self._fmt_btns.append(btn)

        # Window controls
        self._btn_min = tk.Button(ctrl, text="─", font=("Segoe UI", 12),
                                  bg=COLORS["bg2"], fg=COLORS["fg2"],
                                  relief=tk.FLAT, cursor="hand2", padx=8,
                                  command=self._minimize)
        self._btn_min.pack(side=tk.LEFT, padx=2)

        self._btn_fs = tk.Button(ctrl, text="⛶", font=("Segoe UI", 12),
                                 bg=COLORS["bg2"], fg=COLORS["fg2"],
                                 relief=tk.FLAT, cursor="hand2", padx=8,
                                 command=self._toggle_fullscreen)
        self._btn_fs.pack(side=tk.LEFT, padx=2)

        self._btn_close = tk.Button(ctrl, text="✕", font=("Segoe UI", 12),
                                    bg=COLORS["bg2"], fg=COLORS["red"],
                                    relief=tk.FLAT, cursor="hand2", padx=8,
                                    command=self._on_close)
        self._btn_close.pack(side=tk.LEFT, padx=2)

        tk.Button(ctrl, text="⚙", font=("Segoe UI", 14),
                  bg=COLORS["bg2"], fg=COLORS["fg2"],
                  relief=tk.FLAT, cursor="hand2", padx=8,
                  command=self._toggle_options).pack(side=tk.LEFT, padx=5)

    def _change_format(self, fmt):
        self.notes_format = fmt.lower()
        self.config["notes_format"] = self.notes_format
        self._save_config()
        for btn in self._fmt_btns:
            active = btn.cget("text") == fmt
            btn.configure(bg=COLORS["accent2"] if active else COLORS["bg3"],
                          fg="white" if active else COLORS["fg2"])
        self._load_notes()
        self._set_status(f"📝 {fmt} format", COLORS["accent"])

    # =========================================================================
    # SMART ENTRY
    # =========================================================================
    def _build_entry(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg2"], height=60)
        frame.pack(fill=tk.X, pady=(0, 5))
        frame.pack_propagate(False)

        tk.Label(frame, text="⌨", font=("Segoe UI", 18),
                 bg=COLORS["bg2"], fg=COLORS["fg2"]).pack(side=tk.LEFT, padx=(15, 5))

        self.entry = tk.Entry(frame, font=("Segoe UI", 14),
                              bg=COLORS["bg"], fg=COLORS["fg"],
                              insertbackground=COLORS["accent"],
                              relief=tk.FLAT, highlightthickness=1,
                              highlightcolor=COLORS["border"])
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=5)
        self.entry.bind("<Return>", self._process_entry)
        self.entry.bind("<FocusIn>",
                        lambda e: self.entry.configure(highlightcolor=COLORS["accent"]))
        self.entry.bind("<FocusOut>",
                        lambda e: self.entry.configure(highlightcolor=COLORS["border"]))

        self._result_lbl = tk.Label(frame,
                                    text="💡 10 km to miles · 50% of 200 · 0xff to hex",
                                    font=("Segoe UI", 10),
                                    bg=COLORS["bg2"], fg=COLORS["fg2"])
        self._result_lbl.pack(side=tk.RIGHT, padx=15)

    def _process_entry(self, event=None):
        q = self.entry.get().strip()
        if not q:
            return
        result = self._parse(q)
        self._result_lbl.config(text=f"✓ {result}", fg=COLORS["green"])
        self.history.insert(0, f"{q} → {result}")
        self._update_history_list()
        self._save_history()
        self.entry.delete(0, tk.END)
        self._set_status("✓ Processed", COLORS["green"])

    def _parse(self, q):
        q_low = q.lower().strip()

        # Length
        m = re.search(r'(\d+\.?\d*)\s*(mm|cm|m|km|in|ft|yd|mi)\s+(?:to|in)\s+(mm|cm|m|km|in|ft|yd|mi)', q_low)
        if m:
            v, f, t = float(m.group(1)), m.group(2), m.group(3)
            base = CONVERTERS["Length"]["base"]
            if f in base and t in base:
                return f"{v} {f} = {v * base[f] / base[t]:.6g} {t}"

        # Mass
        m = re.search(r'(\d+\.?\d*)\s*(mg|g|kg|t|oz|lb|st)\s+(?:to|in)\s+(mg|g|kg|t|oz|lb|st)', q_low)
        if m:
            v, f, t = float(m.group(1)), m.group(2), m.group(3)
            base = CONVERTERS["Mass"]["base"]
            if f in base and t in base:
                return f"{v} {f} = {v * base[f] / base[t]:.6g} {t}"

        # Temperature
        m = re.search(r'(\d+\.?\d*)\s*([cfk])\s+(?:to|in)\s+([cfk])', q_low)
        if m:
            v, f, t = float(m.group(1)), m.group(2), m.group(3)
            label = {"c": "°C", "f": "°F", "k": "K"}
            c = self._convert_temp(v, label.get(f, f), label.get(t, t))
            if c is not None:
                return f"{v}°{f.upper()} = {c:.4g}°{t.upper()}"

        # Base conversion
        m = re.search(r'(0x[0-9a-f]+|0b[01]+|0o[0-7]+|\d+)\s+to\s+(hex|dec|bin|oct)', q_low)
        if m:
            try:
                n = m.group(1)
                num = int(n, 0)
                t = m.group(2)
                if t == "hex": return f"{n} = 0x{num:X}"
                if t == "bin": return f"{n} = 0b{num:b}"
                if t == "oct": return f"{n} = 0o{num:o}"
                return f"{n} = {num}"
            except Exception:
                pass

        # Percentage
        m = re.search(r'(\d+\.?\d*)\s*%?\s*of\s*(\d+\.?\d*)', q_low)
        if m:
            return f"{m.group(1)}% of {m.group(2)} = {float(m.group(1)) / 100 * float(m.group(2)):.6g}"

        # Math expression
        try:
            expr = re.sub(r'sqrt', 'math.sqrt', q_low)
            expr = re.sub(r'\bpi\b', str(math.pi), expr)
            safe = re.sub(r'[^0-9+\-*/.()% ]', '', expr)
            if safe:
                res = eval(safe, {"__builtins__": {}}, {"math": math})
                return f"{q} = {res}"
        except Exception:
            pass

        return "Try: 10 km to miles · 50% of 200 · 0xff to hex"

    # =========================================================================
    # STATUS BAR
    # =========================================================================
    def _build_status_bar(self):
        bar = tk.Frame(self.main, bg=COLORS["bg2"], height=32)
        bar.pack(fill=tk.X, side=tk.BOTTOM)
        bar.pack_propagate(False)

        self._cursor_ind = tk.Label(bar, text="▌", font=("Segoe UI", 14),
                                    bg=COLORS["bg2"], fg=COLORS["accent"])
        self._cursor_ind.pack(side=tk.LEFT, padx=(10, 5))

        self.status = tk.Label(bar, text="Ready", font=("Segoe UI", 10),
                               bg=COLORS["bg2"], fg=COLORS["fg2"])
        self.status.pack(side=tk.LEFT, padx=(0, 15))

        self._stats_lbl = tk.Label(bar, text="", font=("Segoe UI", 10),
                                   bg=COLORS["bg2"], fg=COLORS["fg3"])
        self._stats_lbl.pack(side=tk.LEFT, padx=15)

        # Update stats every 5 s — not on every keystroke
        def _update_stats():
            try:
                note_len = len(self.notes.get(1.0, tk.END).strip())
                self._stats_lbl.config(text=f"📝 {note_len} chars · {len(self.history)} history")
            except Exception:
                pass
            bar.after(5000, _update_stats)
        _update_stats()

        tk.Label(bar, text="🌀", font=("Segoe UI", 12),
                 bg=COLORS["bg2"],
                 fg=COLORS["accent"] if self.wobble_enabled else COLORS["fg3"]
                 ).pack(side=tk.LEFT, padx=5)

        time_lbl = tk.Label(bar, font=("Segoe UI", 10),
                            bg=COLORS["bg2"], fg=COLORS["fg3"])
        time_lbl.pack(side=tk.RIGHT, padx=18)

        def _tick_time():
            time_lbl.config(text=datetime.now().strftime("%H:%M:%S"))
            bar.after(1000, _tick_time)
        _tick_time()

    # =========================================================================
    # CONVERTER
    # =========================================================================
    def _build_converter(self):
        frame = tk.Frame(self.notebook, bg=COLORS["bg2"])
        self.notebook.add(frame, text="🔄 Converter")

        glass = tk.Frame(frame, bg=COLORS["bg2"])
        glass.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        cat_f = tk.Frame(glass, bg=COLORS["bg2"])
        cat_f.pack(fill=tk.X, pady=8)
        tk.Label(cat_f, text="Category", font=("Segoe UI", 12),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(side=tk.LEFT, padx=(0, 12))
        self._cat_var = tk.StringVar(value="Length")
        cat_cb = ttk.Combobox(cat_f, textvariable=self._cat_var,
                              values=list(CONVERTERS.keys()),
                              state="readonly", width=18, font=("Segoe UI", 11))
        cat_cb.pack(side=tk.LEFT)
        cat_cb.bind("<<ComboboxSelected>>", self._update_units)

        unit_f = tk.Frame(glass, bg=COLORS["bg2"])
        unit_f.pack(fill=tk.X, pady=8)
        tk.Label(unit_f, text="From", font=("Segoe UI", 12),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(side=tk.LEFT, padx=(0, 12))
        self._from_var = tk.StringVar()
        self._from_cb = ttk.Combobox(unit_f, textvariable=self._from_var,
                                     state="readonly", width=12, font=("Segoe UI", 11))
        self._from_cb.pack(side=tk.LEFT, padx=(0, 15))
        tk.Button(unit_f, text="⇄", font=("Segoe UI", 16),
                  bg=COLORS["bg3"], fg=COLORS["fg"], relief=tk.FLAT,
                  cursor="hand2", command=self._swap_units).pack(side=tk.LEFT, padx=5)
        tk.Label(unit_f, text="To", font=("Segoe UI", 12),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(side=tk.LEFT, padx=(15, 12))
        self._to_var = tk.StringVar()
        self._to_cb = ttk.Combobox(unit_f, textvariable=self._to_var,
                                   state="readonly", width=12, font=("Segoe UI", 11))
        self._to_cb.pack(side=tk.LEFT)

        val_f = tk.Frame(glass, bg=COLORS["bg2"])
        val_f.pack(fill=tk.X, pady=8)
        tk.Label(val_f, text="Value", font=("Segoe UI", 12),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(side=tk.LEFT, padx=(0, 12))
        self._val_entry = tk.Entry(val_f, font=("Segoe UI", 14), width=18,
                                   bg=COLORS["bg"], fg=COLORS["fg"],
                                   insertbackground=COLORS["accent"],
                                   relief=tk.FLAT, highlightthickness=1,
                                   highlightcolor=COLORS["border"])
        self._val_entry.pack(side=tk.LEFT, padx=(0, 12))
        self._val_entry.bind("<Return>", self._do_convert)
        tk.Button(val_f, text="Convert", font=("Segoe UI", 12, "bold"),
                  bg=COLORS["accent2"], fg="white", relief=tk.FLAT,
                  cursor="hand2", padx=25, pady=6,
                  command=self._do_convert).pack(side=tk.LEFT)

        res_f = tk.Frame(glass, bg=COLORS["bg2"])
        res_f.pack(fill=tk.BOTH, expand=True, pady=10)
        tk.Label(res_f, text="Result", font=("Segoe UI", 11, "bold"),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(anchor="w", pady=(0, 5))
        self._conv_result = scrolledtext.ScrolledText(res_f, height=3,
                                                      font=("Segoe UI", 16),
                                                      wrap=tk.WORD, bg=COLORS["bg"],
                                                      fg=COLORS["green"], relief=tk.FLAT,
                                                      highlightthickness=1,
                                                      highlightcolor=COLORS["border"])
        self._conv_result.pack(fill=tk.BOTH, expand=True)
        self._conv_result.config(state=tk.DISABLED)

        self._update_units()

    def _update_units(self, event=None):
        units = CONVERTERS.get(self._cat_var.get(), {}).get("units", [])
        self._from_cb["values"] = units
        self._to_cb["values"] = units
        if units:
            self._from_var.set(units[0])
            self._to_var.set(units[1] if len(units) > 1 else units[0])

    def _swap_units(self):
        f, t = self._from_var.get(), self._to_var.get()
        self._from_var.set(t)
        self._to_var.set(f)
        self._do_convert()

    def _do_convert(self, event=None):
        try:
            val = float(self._val_entry.get().strip())
            frm = self._from_var.get()
            to  = self._to_var.get()
            cat = self._cat_var.get()
            data = CONVERTERS.get(cat, {})
            if data.get("special") == "temp":
                result = self._convert_temp(val, frm, to)
                if result is None:
                    raise ValueError
            else:
                base = data.get("base", {})
                if frm not in base or to not in base:
                    raise ValueError
                result = val * base[frm] / base[to]

            txt = f"{val} {frm} = {result:.6g} {to}"
            self.history.insert(0, txt)
            self._update_history_list()
            self._save_history()
        except Exception:
            txt = "❌ Enter a valid number"

        self._conv_result.config(state=tk.NORMAL)
        self._conv_result.delete(1.0, tk.END)
        self._conv_result.insert(tk.END, txt)
        self._conv_result.config(state=tk.DISABLED)
        if not txt.startswith("❌"):
            self._set_status("✓ Converted", COLORS["green"])

    def _convert_temp(self, val, frm, to):
        if frm == "°C":   k = val + 273.15
        elif frm == "°F": k = (val - 32) * 5 / 9 + 273.15
        elif frm == "K":  k = val
        else: return None
        if to == "°C":   return k - 273.15
        elif to == "°F": return (k - 273.15) * 9 / 5 + 32
        elif to == "K":  return k
        return None

    # =========================================================================
    # CALCULATOR
    # =========================================================================
    def _build_calculator(self):
        frame = tk.Frame(self.notebook, bg=COLORS["bg2"])
        self.notebook.add(frame, text="🧮 Calculator")

        glass = tk.Frame(frame, bg=COLORS["bg2"])
        glass.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        self._calc_disp = tk.Entry(glass, font=("Segoe UI", 24), justify="right",
                                   bg=COLORS["bg"], fg=COLORS["fg"],
                                   insertbackground=COLORS["accent"],
                                   relief=tk.FLAT, highlightthickness=1,
                                   highlightcolor=COLORS["border"])
        self._calc_disp.pack(fill=tk.X, pady=5, ipady=12)
        self._calc_disp.bind("<Return>", self._calc_eval)

        btn_f = tk.Frame(glass, bg=COLORS["bg2"])
        btn_f.pack(fill=tk.BOTH, expand=True, pady=8)

        buttons = [
            ["C",  "⌫", "(",  ")"],
            ["7",  "8", "9",  "÷"],
            ["4",  "5", "6",  "×"],
            ["1",  "2", "3",  "−"],
            ["0",  ".", "=",  "+"],
        ]
        for r, row in enumerate(buttons):
            for c, txt in enumerate(row):
                bg = COLORS["bg3"]; fg = COLORS["fg"]
                if txt in ("C", "⌫"):         bg = COLORS["red"];     fg = "white"
                elif txt == "=":               bg = COLORS["accent2"]; fg = "white"
                elif txt in ("÷", "×", "−", "+"): bg = COLORS["bg2"]; fg = COLORS["accent"]
                tk.Button(btn_f, text=txt, font=("Segoe UI", 18, "bold"),
                          bg=bg, fg=fg, relief=tk.FLAT, cursor="hand2",
                          command=lambda t=txt: self._calc_click(t)
                          ).grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
        for i in range(5): btn_f.grid_rowconfigure(i, weight=1)
        for i in range(4): btn_f.grid_columnconfigure(i, weight=1)

        adv_f = tk.Frame(glass, bg=COLORS["bg2"])
        adv_f.pack(fill=tk.X, pady=5)
        for i, (lbl, cmd) in enumerate([("√","sqrt"),("x²","**2"),("π","pi"),
                                         ("e","e"),("sin","sin"),("cos","cos"),("tan","tan")]):
            tk.Button(adv_f, text=lbl, font=("Segoe UI", 10),
                      bg=COLORS["bg3"], fg=COLORS["fg"],
                      relief=tk.FLAT, cursor="hand2",
                      command=lambda c=cmd: self._calc_adv(c)
                      ).grid(row=0, column=i, sticky="nsew", padx=3, pady=3)
            adv_f.grid_columnconfigure(i, weight=1)

        hist_f = tk.Frame(glass, bg=COLORS["bg2"])
        hist_f.pack(fill=tk.X, pady=(5, 0))
        tk.Label(hist_f, text="History", font=("Segoe UI", 10, "bold"),
                 bg=COLORS["bg2"], fg=COLORS["fg2"]).pack(anchor="w", pady=(0, 5))
        self._calc_hist_lb = tk.Listbox(hist_f, height=3, font=("Consolas", 10),
                                         bg=COLORS["bg"], fg=COLORS["fg"],
                                         relief=tk.FLAT, highlightthickness=1,
                                         highlightcolor=COLORS["border"])
        self._calc_hist_lb.pack(fill=tk.X)
        self._calc_hist_lb.bind("<Double-Button-1>", self._calc_hist_use)

        self._calc_input = ""

    def _calc_click(self, val):
        if val == "C":
            self._calc_input = ""
            self._calc_disp.delete(0, tk.END)
        elif val == "⌫":
            self._calc_input = self._calc_input[:-1]
            self._calc_disp.delete(0, tk.END)
            self._calc_disp.insert(0, self._calc_input)
        elif val == "=":
            self._calc_eval()
        else:
            if val == "÷": val = "/"
            elif val == "×": val = "*"
            elif val == "−": val = "-"
            self._calc_input += val
            self._calc_disp.delete(0, tk.END)
            self._calc_disp.insert(0, self._calc_input)

    def _calc_adv(self, cmd):
        if cmd == "sqrt":
            self._calc_input = f"sqrt({self._calc_input or '0'})"
        elif cmd == "**2":
            self._calc_input += "**2"
        elif cmd == "pi":
            self._calc_input += str(math.pi)
        elif cmd == "e":
            self._calc_input += str(math.e)
        elif cmd in ("sin", "cos", "tan"):
            self._calc_input = f"{cmd}({self._calc_input or '0'})"
        self._calc_disp.delete(0, tk.END)
        self._calc_disp.insert(0, self._calc_input)

    def _calc_eval(self, event=None):
        try:
            expr = self._calc_input
            for fn in ("sqrt", "sin", "cos", "tan"):
                expr = expr.replace(fn, f"math.{fn}")
            expr = expr.replace("pi", str(math.pi))
            safe = re.sub(r"[^0-9+\-*/.()% ]", "", expr)
            if safe:
                result = eval(safe, {"__builtins__": {}}, {"math": math})
                display = f"{self._calc_input} = {result}"
                self._calc_disp.delete(0, tk.END)
                self._calc_disp.insert(0, str(result))
                self._calc_hist_lb.insert(0, display)
                self._calc_input = str(result)
        except Exception:
            self._calc_disp.delete(0, tk.END)
            self._calc_disp.insert(0, "Error")

    def _calc_hist_use(self, event):
        sel = self._calc_hist_lb.curselection()
        if sel:
            entry = self._calc_hist_lb.get(sel[0])
            if "=" in entry:
                self._calc_input = entry.split("=")[-1].strip()
                self._calc_disp.delete(0, tk.END)
                self._calc_disp.insert(0, self._calc_input)

    # =========================================================================
    # NOTES
    # =========================================================================
    def _build_notes_tab(self):
        frame = tk.Frame(self.notebook, bg=COLORS["bg2"])
        self.notebook.add(frame, text="📝 Notes")

        glass = tk.Frame(frame, bg=COLORS["bg2"])
        glass.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        toolbar = tk.Frame(glass, bg=COLORS["bg2"])
        toolbar.pack(fill=tk.X, pady=(0, 8))

        for lbl, cmd in [("💾 Save",    self._save_notes),
                          ("📂 Load",    self._load_notes),
                          ("🕐 Timestamp", self._insert_ts),
                          ("🗑️ Clear",   self._clear_notes),
                          ("📋 Copy",    self._copy_notes)]:
            tk.Button(toolbar, text=lbl, font=("Segoe UI", 10),
                      bg=COLORS["bg3"], fg=COLORS["fg"],
                      relief=tk.FLAT, cursor="hand2", padx=12, pady=4,
                      command=cmd).pack(side=tk.LEFT, padx=3)

        # Use tk.Text directly (scrolledtext adds nothing we need and is slightly heavier)
        self.notes = tk.Text(glass, font=("Segoe UI", 13),
                             wrap=tk.WORD, undo=True,
                             bg=COLORS["bg"], fg=COLORS["fg"],
                             relief=tk.FLAT, highlightthickness=1,
                             highlightcolor=COLORS["border"],
                             insertbackground=COLORS["accent"],
                             insertwidth=2, padx=15, pady=15)
        sb = ttk.Scrollbar(glass, command=self.notes.yview)
        self.notes.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.notes.pack(fill=tk.BOTH, expand=True)
        # No per-keystroke cursor restart — the blink timer runs continuously

    def _insert_ts(self):
        self.notes.insert(tk.END, f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
        self.notes.see(tk.END)
        self._set_status("🕐 Timestamp added", COLORS["accent"])

    def _clear_notes(self):
        if messagebox.askyesno("Clear", "Clear all notes?"):
            self.notes.delete(1.0, tk.END)
            self._save_notes()

    def _copy_notes(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.notes.get(1.0, tk.END))
        self._set_status("📋 Copied!", COLORS["green"])

    # =========================================================================
    # HISTORY TAB
    # =========================================================================
    def _build_history_tab(self):
        frame = tk.Frame(self.notebook, bg=COLORS["bg2"])
        self.notebook.add(frame, text="📋 History")

        glass = tk.Frame(frame, bg=COLORS["bg2"])
        glass.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        toolbar = tk.Frame(glass, bg=COLORS["bg2"])
        toolbar.pack(fill=tk.X, pady=(0, 8))

        for lbl, cmd in [("🗑️ Clear",   self._clear_history),
                          ("📤 Export",  self._export_history),
                          ("🔄 Refresh", self._refresh_history)]:
            tk.Button(toolbar, text=lbl, font=("Segoe UI", 10),
                      bg=COLORS["bg3"], fg=COLORS["fg"],
                      relief=tk.FLAT, cursor="hand2", padx=12, pady=4,
                      command=cmd).pack(side=tk.LEFT, padx=3)

        self.history_list = tk.Listbox(glass, font=("Consolas", 11),
                                       bg=COLORS["bg"], fg=COLORS["fg"],
                                       relief=tk.FLAT, highlightthickness=1,
                                       highlightcolor=COLORS["border"],
                                       selectbackground=COLORS["accent2"])
        self.history_list.pack(fill=tk.BOTH, expand=True)
        self.history_list.bind("<Double-Button-1>", self._history_use)
        self.history_list.bind("<Button-3>", self._history_ctx)

    def _update_history_list(self):
        self.history_list.delete(0, tk.END)
        for entry in self.history[:100]:
            self.history_list.insert(tk.END, entry)

    def _history_use(self, event=None):
        sel = self.history_list.curselection()
        if sel:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.history_list.get(sel[0]))
            self._process_entry()

    def _history_ctx(self, event):
        sel = self.history_list.curselection()
        if sel:
            menu = tk.Menu(self.root, tearoff=0, bg=COLORS["bg3"], fg=COLORS["fg"])
            menu.add_command(label="Use",    command=self._history_use)
            menu.add_command(label="Copy",   command=self._copy_history_entry)
            menu.add_separator()
            menu.add_command(label="Delete", command=self._del_history_entry)
            menu.post(event.x_root, event.y_root)

    def _copy_history_entry(self):
        sel = self.history_list.curselection()
        if sel:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.history_list.get(sel[0]))
            self._set_status("📋 Copied!", COLORS["green"])

    def _del_history_entry(self):
        sel = self.history_list.curselection()
        if sel:
            idx = sel[0]
            if 0 <= idx < len(self.history):
                del self.history[idx]
                self._update_history_list()
                self._save_history()

    def _clear_history(self):
        if messagebox.askyesno("Clear", "Clear all history?"):
            self.history = []
            self._update_history_list()
            self._save_history()
            self._set_status("🗑️ History cleared", COLORS["orange"])

    def _export_history(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if path:
            try:
                with open(path, "w") as f:
                    f.write("\n".join(self.history))
                messagebox.showinfo("Success", f"Exported to {path}")
            except Exception:
                messagebox.showerror("Error", "Export failed")

    def _refresh_history(self):
        self.history = self._load_history()
        self._update_history_list()
        self._set_status("🔄 Refreshed", COLORS["accent"])

    # =========================================================================
    # OPTIONS
    # =========================================================================
    def _build_options_tab(self):
        frame = tk.Frame(self.notebook, bg=COLORS["bg2"])
        self.notebook.add(frame, text="⚙️ Options")

        canvas = tk.Canvas(frame, bg=COLORS["bg2"], highlightthickness=0)
        sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=COLORS["bg2"])
        scrollable.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        s = tk.Frame(scrollable, bg=COLORS["bg2"])
        s.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        tk.Label(s, text="⚙️ Settings", font=("Segoe UI", 20, "bold"),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(anchor="w", pady=(0, 20))

        self._sv = {}

        def add_check(label, key, current):
            self._sv[key] = tk.BooleanVar(value=current)
            row = tk.Frame(s, bg=COLORS["bg2"])
            row.pack(fill=tk.X, pady=5)
            ind = tk.Label(row, text="✓" if current else "○",
                           font=("Segoe UI", 12), bg=COLORS["bg2"],
                           fg=COLORS["green"] if current else COLORS["fg3"])
            ind.pack(side=tk.RIGHT)
            def _toggle(*_):
                v = self._sv[key].get()
                ind.config(text="✓" if v else "○",
                           fg=COLORS["green"] if v else COLORS["fg3"])
            self._sv[key].trace("w", _toggle)
            tk.Checkbutton(row, text=label, variable=self._sv[key],
                           bg=COLORS["bg2"], fg=COLORS["fg"],
                           selectcolor=COLORS["bg3"],
                           font=("Segoe UI", 12)).pack(side=tk.LEFT)

        add_check("Auto-save notes and history", "auto_save", self.auto_save_enabled)
        add_check("Blinking cursor in notes",    "cursor_blink", self.cursor_blink)
        add_check("WM Wobble (title bar double-click)", "wobble", self.wobble_enabled)

        fmt_row = tk.Frame(s, bg=COLORS["bg2"])
        fmt_row.pack(fill=tk.X, pady=10)
        tk.Label(fmt_row, text="Notes Format:", font=("Segoe UI", 12),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(side=tk.LEFT, padx=(0, 15))
        self._fmt_var = tk.StringVar(value=self.notes_format.upper())
        for fmt in ("MD", "TXT"):
            tk.Radiobutton(fmt_row, text=fmt, variable=self._fmt_var, value=fmt,
                           bg=COLORS["bg2"], fg=COLORS["fg"],
                           selectcolor=COLORS["bg3"],
                           font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=5)

        tk.Frame(s, bg=COLORS["border"], height=1).pack(fill=tk.X, pady=20)

        info = tk.Frame(s, bg=COLORS["bg2"])
        info.pack(fill=tk.X, pady=10)
        tk.Label(info, text="📁 Data Directory", font=("Segoe UI", 13, "bold"),
                 bg=COLORS["bg2"], fg=COLORS["fg"]).pack(anchor="w")
        tk.Label(info, text="~/.enhanced/", font=("Segoe UI", 11),
                 bg=COLORS["bg2"], fg=COLORS["fg2"]).pack(anchor="w", pady=(2, 10))

        btn_row = tk.Frame(s, bg=COLORS["bg2"])
        btn_row.pack(fill=tk.X, pady=20)
        tk.Button(btn_row, text="💾 Save Settings", font=("Segoe UI", 12, "bold"),
                  bg=COLORS["accent2"], fg="white", relief=tk.FLAT,
                  cursor="hand2", padx=30, pady=8,
                  command=self._save_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="↻ Apply", font=("Segoe UI", 12),
                  bg=COLORS["bg3"], fg=COLORS["fg"], relief=tk.FLAT,
                  cursor="hand2", padx=20, pady=8,
                  command=self._apply_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="⟲ Reset Defaults", font=("Segoe UI", 12),
                  bg=COLORS["bg3"], fg=COLORS["fg"], relief=tk.FLAT,
                  cursor="hand2", padx=20, pady=8,
                  command=self._reset_defaults).pack(side=tk.LEFT, padx=5)

    def _save_settings(self):
        self._apply_settings()
        self._save_config()
        self._set_status("💾 Settings saved!", COLORS["green"])

    def _apply_settings(self):
        self.auto_save_enabled = self._sv["auto_save"].get()
        self.cursor_blink      = self._sv["cursor_blink"].get()
        self.wobble_enabled    = self._sv["wobble"].get()
        self.notes_format      = self._fmt_var.get().lower()

        self.config.update(auto_save=self.auto_save_enabled,
                           cursor_blink=self.cursor_blink,
                           wobble=self.wobble_enabled,
                           notes_format=self.notes_format)

        if self.cursor_blink:
            self._start_cursor_blink()
        else:
            self._stop_cursor_blink()

        # Sync format buttons in title bar
        for btn in self._fmt_btns:
            active = btn.cget("text").lower() == self.notes_format
            btn.configure(bg=COLORS["accent2"] if active else COLORS["bg3"],
                          fg="white" if active else COLORS["fg2"])
        self._load_notes()
        self._set_status("↻ Settings applied", COLORS["accent"])

    def _reset_defaults(self):
        if messagebox.askyesno("Reset", "Reset all settings to defaults?"):
            self._sv["auto_save"].set(True)
            self._sv["cursor_blink"].set(True)
            self._sv["wobble"].set(True)
            self._fmt_var.set("MD")
            self._save_settings()

    def _toggle_options(self):
        self.notebook.select(4)

    # =========================================================================
    # CLOSE
    # =========================================================================
    def _on_close(self):
        self._stop_cursor_blink()
        if self._wobble_job:
            self.root.after_cancel(self._wobble_job)
        if self._glass_job:
            self.root.after_cancel(self._glass_job)
        self._save_notes()
        self._save_history()
        self._save_config()
        self.root.destroy()


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

