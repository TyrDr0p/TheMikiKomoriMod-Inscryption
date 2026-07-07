from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from .schemas import validate_output


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

