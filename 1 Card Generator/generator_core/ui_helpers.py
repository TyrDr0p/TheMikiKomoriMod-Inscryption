from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .schemas import validate_output


class CollapsibleSection(ttk.Frame):
    def __init__(self, master, title: str, expanded: bool = True, **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.expanded = tk.BooleanVar(value=expanded)
        self.columnconfigure(0, weight=1)
        self.header = ttk.Button(self, command=self.toggle)
        self.header.grid(row=0, column=0, sticky="ew", pady=(8, 2))
        self.body = ttk.Frame(self)
        self.body.grid(row=1, column=0, sticky="ew")
        self.body.columnconfigure(1, weight=1)
        self.body.columnconfigure(2, weight=0)
        self._sync()

    def toggle(self):
        self.expanded.set(not self.expanded.get())
        self._sync()

    def _sync(self):
        marker = "[-]" if self.expanded.get() else "[+]"
        self.header.configure(text=f"{marker} {self.title}")
        if self.expanded.get():
            self.body.grid()
        else:
            self.body.grid_remove()


def responsive_column_count(width: int, preferred_columns: int, min_item_width: int) -> int:
    preferred_columns = max(1, preferred_columns)
    min_item_width = max(120, min_item_width)
    if width <= 1:
        return preferred_columns
    return max(1, min(preferred_columns, width // min_item_width))


class ResponsiveCheckboxGroup(ttk.Frame):
    def __init__(self, master, vars_by_key, labels=None, tooltips=None, preferred_columns=3, min_item_width=220, **kwargs):
        super().__init__(master, **kwargs)
        self.vars_by_key = vars_by_key
        self.labels = labels or {}
        self.tooltips = tooltips or {}
        self.preferred_columns = max(1, preferred_columns)
        self.min_item_width = max(120, min_item_width)
        self.checkbuttons = []

        for key, var in vars_by_key.items():
            text = self.labels.get(key, key)
            checkbutton = ttk.Checkbutton(self, text=text, variable=var)
            tooltip = self.tooltips.get(key, "")
            if tooltip:
                ToolTip(checkbutton, tooltip)
            self.checkbuttons.append(checkbutton)

        self.bind("<Configure>", self._layout_items)
        self._layout_items()

    def _layout_items(self, _event=None):
        columns = responsive_column_count(self.winfo_width(), self.preferred_columns, self.min_item_width)

        for index in range(self.preferred_columns):
            self.columnconfigure(index, weight=0)
        for index in range(columns):
            self.columnconfigure(index, weight=1, uniform="checkbox")

        for index, checkbutton in enumerate(self.checkbuttons):
            checkbutton.grid(row=index // columns, column=index % columns, sticky=tk.W, padx=(0, 12), pady=1)


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window or not self.text:
            return
        x = (event.x_root if event else self.widget.winfo_pointerx()) + 15
        y = (event.y_root if event else self.widget.winfo_pointery()) + 15
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 9),
        )
        label.pack()

    def hide(self, _event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def choose_image(path_var):
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
    )
    if file_path:
        path_var.set(file_path)


def choose_audio(path_var):
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.aiff *.aif"), ("All files", "*.*")]
    )
    if file_path:
        path_var.set(file_path)


def set_text(widget: tk.Text, value: str):
    widget.config(state=tk.NORMAL)
    widget.delete("1.0", tk.END)
    widget.insert("1.0", value)
    widget.config(state=tk.DISABLED)


def update_json_preview(text_widget: tk.Text, status_var: tk.StringVar, schema_kind: str, data: dict):
    formatted = json.dumps(data, indent=4, ensure_ascii=False)
    set_text(text_widget, formatted)
    errors = validate_output(schema_kind, data)
    if errors:
        status_var.set("Validation errors: " + " | ".join(errors[:3]))
    else:
        status_var.set("Valid JSONCardLoader output.")
    return errors


def save_json_file(schema_kind: str, data: dict, initialfile: str, success_label: str):
    errors = validate_output(schema_kind, data)
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors[:8]))
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".jldr2",
        filetypes=[("JSON Card Loader 2", "*.jldr2"), ("All Files", "*.*")],
        initialfile=initialfile,
    )
    if not file_path:
        return
    try:
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=4, ensure_ascii=False)
        messagebox.showinfo("Success", f"{success_label} saved to:\n{file_path}")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to save: {exc}")
