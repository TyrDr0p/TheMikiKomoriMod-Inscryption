from __future__ import annotations

import logging
import tkinter as tk
from tkinter import ttk


logger = logging.getLogger(__name__)


def mousewheel_units(event) -> int:
    if getattr(event, "num", None) == 4:
        return -3
    if getattr(event, "num", None) == 5:
        return 3
    delta = getattr(event, "delta", 0)
    if delta == 0:
        return 0
    if abs(delta) >= 120:
        return int(-delta / 120)
    return -1 if delta > 0 else 1


class ScrollableFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content.bind("<Configure>", self._on_content_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind_all("<MouseWheel>", self._on_mousewheel, add="+")
        self.bind_all("<Button-4>", self._on_mousewheel, add="+")
        self.bind_all("<Button-5>", self._on_mousewheel, add="+")

    def _on_content_configure(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _pointer_inside(self) -> bool:
        try:
            widget = self.winfo_containing(self.winfo_pointerx(), self.winfo_pointery())
        except (KeyError, tk.TclError) as exc:
            logger.debug("Ignoring mousewheel over non-app Tk window: %s", exc)
            return False
        while widget is not None:
            if widget is self:
                return True
            widget = getattr(widget, "master", None)
        return False

    def _on_mousewheel(self, event):
        if not self._pointer_inside():
            return
        units = mousewheel_units(event)
        if units:
            self.canvas.yview_scroll(units, "units")

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)
