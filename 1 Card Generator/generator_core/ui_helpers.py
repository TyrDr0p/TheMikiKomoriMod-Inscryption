from __future__ import annotations

import json
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .schemas import validate_output


logger = logging.getLogger(__name__)


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
        logger.debug("Toggled section title=%r expanded=%s", self.title, self.expanded.get())
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


def clamp_sash_position(position: int, total_width: int, min_form_width: int, min_preview_width: int) -> int:
    if total_width <= 1:
        return position

    min_form_width = max(1, min_form_width)
    min_preview_width = max(1, min_preview_width)
    max_form_width = max(1, total_width - min_preview_width)
    if max_form_width < min_form_width:
        return max_form_width
    return min(max(position, min_form_width), max_form_width)


def default_sash_position(total_width: int, preview_ratio: float, min_form_width: int, min_preview_width: int) -> int:
    preview_ratio = min(max(preview_ratio, 0.05), 0.8)
    position = round(total_width * (1 - preview_ratio))
    return clamp_sash_position(position, total_width, min_form_width, min_preview_width)


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
        item_width = self._minimum_column_width()
        columns = responsive_column_count(self.winfo_width(), self.preferred_columns, item_width)
        previous_columns = getattr(self, "_last_columns", None)
        if previous_columns != columns:
            logger.debug(
                "Responsive checkbox layout changed width=%s item_width=%s preferred_columns=%s columns=%s item_count=%s",
                self.winfo_width(),
                item_width,
                self.preferred_columns,
                columns,
                len(self.checkbuttons),
            )
            self._last_columns = columns

        for index in range(self.preferred_columns):
            self.columnconfigure(index, weight=0, minsize=0, uniform="")
        for index in range(columns):
            self.columnconfigure(index, weight=0, minsize=item_width, uniform="")

        for index, checkbutton in enumerate(self.checkbuttons):
            checkbutton.grid(row=index // columns, column=index % columns, sticky=tk.W, padx=(0, 12), pady=1)

    def _minimum_column_width(self):
        requested_widths = [checkbutton.winfo_reqwidth() + 18 for checkbutton in self.checkbuttons]
        return max([self.min_item_width, *requested_widths])


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
    logger.debug("Opening image picker")
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
    )
    if file_path:
        logger.info("Selected image file: %s", file_path)
        path_var.set(file_path)
    else:
        logger.debug("Image picker cancelled")


def choose_audio(path_var):
    logger.debug("Opening audio picker")
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.aiff *.aif"), ("All files", "*.*")]
    )
    if file_path:
        logger.info("Selected audio file: %s", file_path)
        path_var.set(file_path)
    else:
        logger.debug("Audio picker cancelled")


def set_text(widget: tk.Text, value: str):
    widget.config(state=tk.NORMAL)
    widget.delete("1.0", tk.END)
    widget.insert("1.0", value)
    widget.config(state=tk.DISABLED)


def update_json_preview(text_widget: tk.Text, status_var: tk.StringVar, schema_kind: str, data: dict):
    formatted = json.dumps(data, indent=4, ensure_ascii=False)
    logger.debug("Updating JSON preview kind=%s bytes=%s data=%s", schema_kind, len(formatted), formatted)
    set_text(text_widget, formatted)
    errors = validate_output(schema_kind, data)
    if errors:
        status_var.set("Validation errors: " + " | ".join(errors[:3]))
        logger.info("Preview validation failed kind=%s error_count=%s first_errors=%s", schema_kind, len(errors), errors[:3])
    else:
        status_var.set("Valid JSONCardLoader output.")
        logger.debug("Preview validation passed kind=%s", schema_kind)
    return errors


def save_json_file(schema_kind: str, data: dict, initialfile: str, success_label: str):
    logger.info("Save requested kind=%s initialfile=%s", schema_kind, initialfile)
    logger.debug("Save data kind=%s data=%s", schema_kind, json.dumps(data, indent=2, ensure_ascii=False))
    errors = validate_output(schema_kind, data)
    if errors:
        logger.warning("Save blocked by validation errors kind=%s error_count=%s errors=%s", schema_kind, len(errors), errors)
        messagebox.showerror("Validation Error", "\n".join(errors[:8]))
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".jldr2",
        filetypes=[("JSON Card Loader 2", "*.jldr2"), ("All Files", "*.*")],
        initialfile=initialfile,
    )
    if not file_path:
        logger.info("Save cancelled kind=%s", schema_kind)
        return
    try:
        with open(file_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=4, ensure_ascii=False)
        logger.info("Saved %s to %s", success_label, file_path)
        messagebox.showinfo("Success", f"{success_label} saved to:\n{file_path}")
    except Exception as exc:
        logger.exception("Failed to save %s to %s", success_label, file_path)
        messagebox.showerror("Error", f"Failed to save: {exc}")
