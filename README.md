# Lazy Scroller

Control your mouse cursor, scroll, and click using hand gestures — no touching the mouse required.

Built with Python, OpenCV, and MediaPipe's hand landmark model.

## Gestures

| Gesture | Action |
|---|---|
| Index finger up | Move cursor |
| Index + middle up | Scroll (up/down based on position) |
| Pinch (index + thumb close) | Click |
| Double pinch (two pinches quickly) | Double-click |

## Requirements

- Windows (uses `cv2.CAP_DSHOW` for webcam; remove that flag on Linux/Mac)
- Python 3.9–3.11
- A webcam

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Press **Q** to quit.

## Configuration

All tunable settings are at the top of `main.py`:

- `PINCH_DISTANCE_THRESHOLD` — how tight a pinch triggers a click
- `SCROLL_MULTIPLIER` — scroll speed
- `SMOOTHENING` — cursor smoothing (higher = slower but steadier)
- `USE_SMALL_LOW_FATIGUE_BOX` — smaller tracking zone for less arm movement
