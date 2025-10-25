import re
from tkinter import font as tk_font

from abpl.lib import library
from gui.tools_misc import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui_main import MainWindow

FONT = None
PATTERN = None
SEPARATORS = r'[\s\t(),;:{}\[\]#]'


def highlight_line(text_widget, line_number):
    global FONT, PATTERN

    if FONT is None:
        base_font = tk_font.Font(font=text_widget['font'])
        FONT = tk_font.Font(family=base_font.actual()['family'],
                            size=base_font.actual()['size'],
                            weight="bold")

    if PATTERN is None:
        words_pattern = "|".join(re.escape(keyword) for keyword in library.keys())
        PATTERN = rf'(?:(?<=^)|(?<={SEPARATORS}))({words_pattern})(?=$|{SEPARATORS})'

    start_index = f"{line_number}.0"
    end_index = f"{line_number}.end"

    line_text = text_widget.get(start_index, end_index)

    for tag in text_widget.tag_names():
        text_widget.tag_remove(tag, start_index, end_index)

    for match in re.finditer(PATTERN, line_text):
        s = f"{line_number}.{match.start(1)}"
        e = f"{line_number}.{match.end(1)}"
        text_widget.tag_add("keyword", s, e)

    text_widget.tag_config("keyword", foreground="dark blue", font=FONT)


def clear_highlighting(text_widget):
    for tag in text_widget.tag_names():
        text_widget.tag_remove(tag, "1.0", "end")


def edit_abpl(window: "MainWindow"):
    def check_selected():
        try:
            sel1 = edit_field.index("sel.first")
            sel2 = edit_field.index("sel.last")
            return sel1 != sel2
        except tk.TclError:
            return False

    def on_key_release(_=None):
        nonlocal line_amt
        window.f_tweak.abpl.script = edit_field.get("1.0", "end").strip()

        if not high_keyword.get():
            return

        if check_selected():
            return

        current_line_count = int(edit_field.index('end-1c').split('.')[0])
        if current_line_count != line_amt:
            for line in range(1, current_line_count + 1):
                highlight_line(edit_field, line)
            line_amt = current_line_count
        else:
            line_number = edit_field.index("insert").split('.')[0]
            highlight_line(edit_field, line_number)

    def keyword_mode():
        nonlocal line_amt

        if high_keyword.get():
            line_amt = -1
            on_key_release()
        else:
            clear_highlighting(edit_field)

    root = tk.Toplevel(window.root)
    root.title("Edit ABPL script")
    root.geometry("640x480")
    apply_window_style(root, resize_w=True, resize_h=True)
    root.grab_set()
    root.focus_force()
    root.bind("<Escape>", lambda event: root.destroy())

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    line_amt = -1
    edit_field = tk.Text(root, wrap="none")
    scroll_x = ttk.Scrollbar(root, command=edit_field.xview, orient="horizontal")
    scroll_y = ttk.Scrollbar(root, command=edit_field.yview, orient="vertical")

    edit_field.grid(row=1, column=0, sticky="news")
    scroll_x.grid(row=2, column=0, sticky="ew")
    scroll_y.grid(row=1, column=1, sticky="ns")

    high_keyword = CCheckbox(root, text="Highlight keywords")
    high_keyword.root.configure(command=keyword_mode)
    high_keyword.root.grid(row=0, column=0, columnspan=2, sticky="w", padx=1, pady=1)

    edit_field.bind('<KeyRelease>', on_key_release)
    edit_field.bind('<<Paste>>', on_key_release)
    edit_field.config(xscrollcommand=scroll_x.set)
    edit_field.config(yscrollcommand=scroll_y.set)

    edit_field.insert("1.0", window.f_tweak.abpl.script)
    edit_field.mark_set("insert", "1.0")
    edit_field.focus_set()

    high_keyword.set(len(window.f_tweak.abpl.script) < 8*1024)
    on_key_release()
