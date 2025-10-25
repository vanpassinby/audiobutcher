import tkinter.ttk as ttk


class LimitedEntry(ttk.Entry):
    def __init__(self, parent, role: str, width=3):
        super().__init__(parent, width=width)
        self.role = role

        if role != "h":
            self.bind("<Left>", self.on_left)
            self.bind("<BackSpace>", lambda _: self.on_left(erase=True))
        if role != "s":
            self.bind("<KeyRelease>", self.check_limit)
            self.bind("<<Paste>>", self.check_limit)
            self.bind("<Right>", self.on_right)

    def on_left(self, _=None, erase=False):
        if self.index("insert") == 0:
            prev_w = self.tk_focusPrev()

            if erase:
                txt_len = len(prev_w.get())
                if txt_len:
                    prev_w.delete(txt_len-1, "end")

            prev_w.icursor("end")
            prev_w.focus()

    def on_right(self, _):
        if self.index("insert") == len(self.get()):
            next_w = self.tk_focusNext()
            next_w.icursor(0)
            next_w.focus()

    def check_limit(self, _=None, switch=True):
        text = self.get()
        if self.role != "s" and len(text) > 2:
            next_w = self.tk_focusNext()

            self.delete(2, "end")
            next_w.insert(0, text[2])

            if switch:
                next_w.focus()
                next_w.icursor(1)

            if self.role == "h":
                next_w.check_limit(switch=False)


class TimeEntry:
    def part_label(self, text):
        return ttk.Label(self.root, text=text, width=2, anchor="center")

    def __init__(self, parent):
        self.root = ttk.Frame(parent, padding=2, borderwidth=1, relief="solid")
        self.hours = LimitedEntry(self.root, role="h")
        self.minutes = LimitedEntry(self.root, role="m")
        self.seconds = LimitedEntry(self.root, role="s", width=6)

        self.hours.pack(side="left")
        self.part_label("h").pack(side="left")
        self.minutes.pack(side="left")
        self.part_label("m").pack(side="left")
        self.seconds.pack(side="left")
        self.part_label("s").pack(side="left")

    def grid(self, **kwargs):
        self.root.grid(**kwargs)

    def configure(self, state):
        self.hours.configure(state=state)
        self.minutes.configure(state=state)
        self.seconds.configure(state=state)

    def set(self, value):
        try:
            value = abs(float(value))
        except ValueError:
            value = 0

        leftover = value - int(value)
        value = min(int(value), 100*3600-1)

        h = value // 3600
        m = value % 3600 // 60
        s = value % 60

        if leftover:
            s += round(leftover, 3)

        self.hours.insert(0, str(h))
        self.minutes.insert(0, str(m))
        self.seconds.insert(0, str(s))

    def get(self):
        h = float(self.hours.get())
        m = float(self.minutes.get())
        s = float(self.seconds.get())
        return h * 3600 + m * 60 + s
