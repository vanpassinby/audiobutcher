python3 -m PyInstaller ../ab401p.py \
  --onefile --noconsole \
  --collect-all tkinterdnd2 \
  --hidden-import='PIL._tkinter_finder' \
  --add-data res/example_data:librosa/util/example_data
