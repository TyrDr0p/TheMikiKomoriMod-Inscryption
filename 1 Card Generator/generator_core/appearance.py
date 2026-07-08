from __future__ import annotations

import ctypes
import ctypes.util
import logging
import platform
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

from .schemas import project_root


logger = logging.getLogger(__name__)

BASE_FONT_FAMILY = "DejaVu Sans"
MONO_FONT_FAMILY = "DejaVu Sans Mono"
BUNDLED_FONT_FILES = ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSansMono.ttf")
_LINUX_FONTCONFIG_REF = None

PALETTES = {
    "light": {
        "bg": "#f2f2f2",
        "panel": "#ffffff",
        "field": "#ffffff",
        "fg": "#111111",
        "muted": "#5b5b5b",
        "accent": "#2f5f9f",
        "button": "#e8e8e8",
        "button_active": "#d8e7f7",
        "select": "#cfe4ff",
        "status": "#6a3b00",
        "border": "#b8b8b8",
    },
    "dark": {
        "bg": "#202124",
        "panel": "#2a2d31",
        "field": "#17191c",
        "fg": "#f0f0f0",
        "muted": "#c5c9cf",
        "accent": "#8ab4f8",
        "button": "#353941",
        "button_active": "#3f4f66",
        "select": "#385d8a",
        "status": "#f5c26b",
        "border": "#555a64",
    },
}


def fonts_dir() -> Path:
    return project_root() / "assets" / "fonts"


def bundled_font_paths() -> list[Path]:
    directory = fonts_dir()
    paths = [directory / filename for filename in BUNDLED_FONT_FILES if (directory / filename).exists()]
    logger.debug("Bundled font paths directory=%s paths=%s", directory, paths)
    return paths


def register_bundled_fonts() -> bool:
    paths = bundled_font_paths()
    if not paths:
        logger.warning("No bundled font files found in %s", fonts_dir())
        return False

    system = platform.system().lower()
    logger.debug("Registering bundled fonts system=%s path_count=%s", system, len(paths))
    if system == "windows":
        result = _register_windows_fonts(paths)
    elif system == "darwin":
        result = _register_macos_fonts(paths)
    elif system == "linux":
        result = _register_linux_fonts(paths)
    else:
        result = False
    logger.info("Bundled font registration system=%s success=%s", system, result)
    return result


def _register_windows_fonts(paths: list[Path]) -> bool:
    try:
        add_font = ctypes.windll.gdi32.AddFontResourceExW
    except AttributeError:
        logger.exception("Windows AddFontResourceExW unavailable")
        return False
    add_font.argtypes = [ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_void_p]
    add_font.restype = ctypes.c_int
    added = False
    for path in paths:
        result = bool(add_font(str(path), 0x10, None))
        logger.debug("Windows font registration path=%s success=%s", path, result)
        added = result or added
    return added


def _register_macos_fonts(paths: list[Path]) -> bool:
    try:
        core_foundation = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
        core_text = ctypes.CDLL("/System/Library/Frameworks/CoreText.framework/CoreText")
    except OSError:
        logger.exception("macOS CoreFoundation/CoreText unavailable for font registration")
        return False

    core_foundation.CFURLCreateFromFileSystemRepresentation.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_long,
        ctypes.c_bool,
    ]
    core_foundation.CFURLCreateFromFileSystemRepresentation.restype = ctypes.c_void_p
    core_foundation.CFRelease.argtypes = [ctypes.c_void_p]
    core_text.CTFontManagerRegisterFontsForURL.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]
    core_text.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool

    added = False
    for path in paths:
        path_bytes = str(path).encode("utf-8")
        url = core_foundation.CFURLCreateFromFileSystemRepresentation(None, path_bytes, len(path_bytes), False)
        if not url:
            logger.debug("macOS font URL creation failed path=%s", path)
            continue
        result = bool(core_text.CTFontManagerRegisterFontsForURL(url, 1, None))
        logger.debug("macOS font registration path=%s success=%s", path, result)
        added = result or added
        core_foundation.CFRelease(url)
    return added


def _register_linux_fonts(paths: list[Path]) -> bool:
    global _LINUX_FONTCONFIG_REF

    library = ctypes.util.find_library("fontconfig")
    if not library:
        logger.warning("fontconfig library not found; skipping Linux private font registration")
        return False
    logger.debug("Using fontconfig library: %s", library)
    try:
        fontconfig = ctypes.CDLL(library)
    except OSError:
        logger.exception("Failed to load fontconfig library: %s", library)
        return False

    fontconfig.FcConfigCreate.argtypes = []
    fontconfig.FcConfigCreate.restype = ctypes.c_void_p
    fontconfig.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    fontconfig.FcConfigAppFontAddFile.restype = ctypes.c_bool
    fontconfig.FcConfigBuildFonts.argtypes = [ctypes.c_void_p]
    fontconfig.FcConfigBuildFonts.restype = ctypes.c_bool
    fontconfig.FcConfigSetCurrent.argtypes = [ctypes.c_void_p]
    fontconfig.FcConfigSetCurrent.restype = ctypes.c_bool

    config = fontconfig.FcConfigCreate()
    if not config:
        logger.warning("FcConfigCreate failed")
        return False

    added = False
    for path in paths:
        result = bool(fontconfig.FcConfigAppFontAddFile(config, str(path).encode("utf-8")))
        logger.debug("Linux private font registration path=%s success=%s", path, result)
        added = result or added
    if not added:
        logger.warning("No Linux bundled fonts were added to private Fontconfig config")
        return False

    if not fontconfig.FcConfigBuildFonts(config):
        logger.warning("FcConfigBuildFonts failed")
        return False
    if not fontconfig.FcConfigSetCurrent(config):
        logger.warning("FcConfigSetCurrent failed")
        return False

    _LINUX_FONTCONFIG_REF = (fontconfig, config)
    logger.debug("Linux private Fontconfig config is current: %s", config)
    return True


def configure_named_fonts(root: tk.Tk) -> tuple[str, str]:
    registration_success = register_bundled_fonts()
    families = {family.lower(): family for family in tkfont.families(root)}
    base_family = families.get(BASE_FONT_FAMILY.lower(), tkfont.nametofont("TkDefaultFont", root=root).actual("family"))
    mono_family = families.get(MONO_FONT_FAMILY.lower(), tkfont.nametofont("TkFixedFont", root=root).actual("family"))
    logger.info(
        "Configured Tk fonts base=%r mono=%r bundled_registration=%s available_family_count=%s",
        base_family,
        mono_family,
        registration_success,
        len(families),
    )

    font_settings = {
        "TkDefaultFont": (base_family, 10),
        "TkTextFont": (base_family, 10),
        "TkMenuFont": (base_family, 10),
        "TkHeadingFont": (base_family, 11),
        "TkCaptionFont": (base_family, 10),
        "TkSmallCaptionFont": (base_family, 9),
        "TkIconFont": (base_family, 10),
        "TkTooltipFont": (base_family, 9),
        "TkFixedFont": (mono_family, 10),
    }
    for name, (family, size) in font_settings.items():
        try:
            tkfont.nametofont(name, root=root).configure(family=family, size=size)
            logger.debug("Configured named font %s family=%s size=%s", name, family, size)
        except tk.TclError:
            logger.exception("Failed to configure named font: %s", name)
            continue
    return base_family, mono_family


class AppearanceManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style(root)
        self.base_family, self.mono_family = configure_named_fonts(root)
        try:
            self.style.theme_use("clam")
            logger.debug("Using ttk theme: clam")
        except tk.TclError:
            logger.exception("Failed to use ttk clam theme; keeping current theme")
            pass

    def apply(self, theme_name: str):
        palette = PALETTES.get(theme_name, PALETTES["light"])
        logger.info("Applying appearance theme=%s", theme_name)
        self.root.configure(background=palette["bg"])
        self._apply_options(palette)
        self._apply_ttk_styles(palette)
        self._apply_widget_colors(self.root, palette)

    def _apply_options(self, palette: dict[str, str]):
        self.root.option_add("*Font", "TkDefaultFont")
        self.root.option_add("*Background", palette["bg"])
        self.root.option_add("*Foreground", palette["fg"])
        self.root.option_add("*selectBackground", palette["select"])
        self.root.option_add("*selectForeground", palette["fg"])
        self.root.option_add("*insertBackground", palette["fg"])
        self.root.option_add("*TCombobox*Listbox.background", palette["field"])
        self.root.option_add("*TCombobox*Listbox.foreground", palette["fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", palette["select"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", palette["fg"])

    def _apply_ttk_styles(self, palette: dict[str, str]):
        self.style.configure(".", font="TkDefaultFont", background=palette["bg"], foreground=palette["fg"])
        self.style.configure("TFrame", background=palette["bg"])
        self.style.configure("Toolbar.TFrame", background=palette["bg"])
        self.style.configure("TLabel", background=palette["bg"], foreground=palette["fg"])
        self.style.configure("Status.TLabel", background=palette["bg"], foreground=palette["status"])
        self.style.configure("TButton", background=palette["button"], foreground=palette["fg"], bordercolor=palette["border"])
        self.style.map(
            "TButton",
            background=[("active", palette["button_active"]), ("pressed", palette["select"])],
            foreground=[("disabled", palette["muted"])],
        )
        self.style.configure("TCheckbutton", background=palette["bg"], foreground=palette["fg"])
        self.style.map(
            "TCheckbutton",
            background=[("active", palette["bg"])],
            foreground=[("disabled", palette["muted"])],
        )
        self.style.configure("TNotebook", background=palette["bg"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=palette["button"], foreground=palette["fg"], padding=(10, 4))
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", palette["panel"]), ("active", palette["button_active"])],
            foreground=[("selected", palette["fg"]), ("disabled", palette["muted"])],
        )
        self.style.configure(
            "TEntry",
            fieldbackground=palette["field"],
            foreground=palette["fg"],
            insertcolor=palette["fg"],
            bordercolor=palette["border"],
        )
        self.style.map(
            "TEntry",
            fieldbackground=[("readonly", palette["field"]), ("!disabled", palette["field"])],
            foreground=[("readonly", palette["fg"]), ("!disabled", palette["fg"])],
        )
        self.style.configure(
            "TSpinbox",
            fieldbackground=palette["field"],
            background=palette["button"],
            foreground=palette["fg"],
            insertcolor=palette["fg"],
            arrowcolor=palette["fg"],
            bordercolor=palette["border"],
        )
        self.style.map(
            "TSpinbox",
            fieldbackground=[("readonly", palette["field"]), ("!disabled", palette["field"])],
            foreground=[("readonly", palette["fg"]), ("!disabled", palette["fg"])],
            background=[("active", palette["button_active"])],
            arrowcolor=[("disabled", palette["muted"]), ("!disabled", palette["fg"])],
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=palette["field"],
            background=palette["button"],
            foreground=palette["fg"],
            arrowcolor=palette["fg"],
            insertcolor=palette["fg"],
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", palette["field"])],
            foreground=[("readonly", palette["fg"])],
            background=[("active", palette["button_active"])],
        )
        self.style.configure("Vertical.TScrollbar", background=palette["button"], troughcolor=palette["bg"])
        self.style.configure("Horizontal.TScrollbar", background=palette["button"], troughcolor=palette["bg"])
        self.style.configure("TPanedwindow", background=palette["bg"])
        self.style.configure("Sash", background=palette["border"])

    def _apply_widget_colors(self, widget: tk.Widget, palette: dict[str, str]):
        if isinstance(widget, tk.Text):
            widget.configure(
                background=palette["field"],
                foreground=palette["fg"],
                insertbackground=palette["fg"],
                selectbackground=palette["select"],
                selectforeground=palette["fg"],
                font="TkFixedFont",
            )
        elif isinstance(widget, tk.Canvas):
            widget.configure(background=palette["bg"])
        elif isinstance(widget, tk.Tk):
            widget.configure(background=palette["bg"])

        for child in widget.winfo_children():
            self._apply_widget_colors(child, palette)
