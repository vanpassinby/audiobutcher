# AudioButcher 4.0 - Launch variables
| Variable | Description |
|---|---|
| `AB_FORCE_CUSTOM_OS` | Force AB to use custom OS API.<br>*Cannot be modified via enviroment variables.* |
| `AB_ANDROID_MODE` | Allows you to quickly run AB on Android using *PyDroid IDE*.<br>*Cannot be modified via enviroment variables.* |
| `AB_DISABLE_ICON` | Disable AudioButhcher window icon. |
| `AB_RESIZABLE_WINDOWS` | Enable resizable windows. |
| `AB_VISUAL_ONSETS_ALL` | In *slice length statistics graph*, show full onset range. |
| `AB_HIDE_TOOLTIPS` | Disable *quick help* tooltips. |
| `AB_FLOAT16_AUDIO` | Use `float16` format instead of `float32` for storing audio in memory.<br>It takes twice less memory, but usually it's slower since `float16` is unoptimised. |
| `AB_NO_INTERPOLATION` | Disable linear interpolation when resampling audio.<br>It makes resampling faster, but creates weird effects. |
| `AB_ABPL_DEBUG` | Log *ABPL* debug onto console. This is has effect when running AB from source code. |
| `AB_DISABLE_TKDND2` | Disable `TkinterDnD2` python library, which is resposible for window Drag'n'Drop. |
| `AB_DISABLE_FFMPEG` | Do not try calling `ffmpeg` when importing audio. |
| `AB_DISABLE_SOUNDFILE` | Disable `soundfile` python library, which allows importing MP3/OGG/FLAC files without `ffmpeg`.<br>(WAV files still can be imported/exported). |
| `AB_DISABLE_SIMPLEAUDIO` | Disable `simpleaudio` python library, which is responsible for preview playback. |
| `AB_DISABLE_PSUTIL` | Disable `psutil` pyhton library, which is responsible for checking if there's enough memory for scrambling. |
| `AB_DISABLE_LIBROSA` | Disable `librosa` python library, which is responsible for detecting onsets in *Default* and *Classic* modes. |
| `AB_DISABLE_PRETTY_MIDI` | Disable `PrettyMIDI` python library, which is responsible for turning MIDI files into slice data. |
| `AB_LIBROSA_SR` | Sample rate used during detecting onsets in *Default* mode.<br>The default value is `22050`, use `0` to disable resampling. |
| `AB_LIBROSA_N_FFT` | `N_FFT` *librosa* parameter used during detecting onsets in *Default* mode.<br>The default value is `1024`. |
| `AB_AMP_ONSET_SR` | Sample rate used during detecting onsets in *Amplitude-based* modes.<br>The default value is `44100`, use `0` to disable resampling. |
| `AB_AMP_ONSET_HOP` | *Hop size* used during detecting onsets in *Amplitude-based* modes.<br>The default value is `512`. |
| `AB_AMP_ONSET_WINDOW` | *Window size* used during detecting onsets in *Amplitude* modes.<br>The default value is `1024`. |
## What is this
* These parameters are used during AB launch, allowing to tweak some of its parameters before it starts.
* The similar parameters were present since AB v2.2, but back then it was only possible to alter them by editing source code.\
  Now it's possible to edit most of them by changing the enviroment variables (e.g. using `set` command in Windows, and `export` in Linux/macOS/BSD).\
  `AB_FORCE_CUSTOM_OS` and `AB_ANDROID_MODE` are toggleable only via the source code editing.
