python -m PyInstaller ..\ab400p.py ^
--onefile ^
--noconsole ^
--icon res\icon.ico ^
--version-file res\version.txt ^
--collect-all tkinterdnd2 ^
--add-data res\example_data;librosa\util\example_data

pause
