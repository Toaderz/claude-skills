# Video and audio

## Nothing is installed, and that is checked

Verified absent in a stock Claude Code remote session:

| Tool | For | Status |
|---|---|---|
| `ffmpeg` | video → frames, audio extraction, format conversion | **absent** |
| `whisper` / `whisper.cpp` | local speech-to-text, no API key, no cost | **absent** |
| `pandoc` | document conversion | **absent** |
| `tesseract` | OCR outside the built-in `pdf` skill | **absent** |

**A capability that depends on these must detect the absence and report it.** The eval
case `11-video` exists to assert that: given a video, the correct behaviour is to say
`ffmpeg` is not available, not to fake a description of the contents.

## The approach when they are installed

**Video → native vision.** There is no video model to call. Extract frames with `ffmpeg`
and read them as images:

```bash
ffmpeg -i input.mp4 -vf fps=1/10 frames/%03d.png    # one frame per 10 seconds
```

Sample by scene change rather than fixed interval when the footage is uneven:

```bash
ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)'" -vsync vfr frames/%03d.png
```

**Audio → local transcription.** `whisper.cpp` runs on CPU, needs no API key, and sends
nothing anywhere:

```bash
ffmpeg -i input.mp4 -ar 16000 -ac 1 audio.wav
whisper-cli -m models/ggml-base.en.bin -f audio.wav
```

Local matters here for more than cost: a recording of a meeting is not something to hand
to a third-party API by default.

## Installing them — your machine, your call

```bash
# macOS
brew install ffmpeg whisper-cpp pandoc tesseract

# Debian / Ubuntu
sudo apt install ffmpeg pandoc tesseract-ocr
# whisper.cpp: build from https://github.com/ggerganov/whisper.cpp
```

**There is no media skill in this library** and there should not be one until the tools
exist. A skill whose every path ends in "the tool is not installed" is ambient cost
buying a error message.
