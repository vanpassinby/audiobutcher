import sys
import common
from gui.gui_main import MainWindow
from gui.tools import dnd_open_file, upd_ffmpeg_path


if common.AB_ANDROID_MODE:
    import tkinter
    tkinter.Tk().withdraw()

window = MainWindow()
window.update_global()
upd_ffmpeg_path(window)
window.cmd_default_settings()

for arg in sys.argv[1:]:
    dnd_open_file(window, arg, aud_load_alter_slices=False)

window.root.mainloop()
sys.exit(0)
