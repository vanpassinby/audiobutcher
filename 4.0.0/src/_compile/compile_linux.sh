python3 -m PyInstaller ../ab400p.py \
  --onefile --noconsole \
  --collect-all tkinterdnd2 \
  --add-data res/example_data:librosa/util/example_data
