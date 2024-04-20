# Download youtube videos

The script in this repo reads video urls from a file `videos.txt` and downloads to folders specified by a path-mapping dictionary defined in `chanpath.json`. It sends a notification via the `notify-send` utility

## Setup

Install `yt-dlp` via

```
pip install yt-dlp
```

and then run

```
python ydp.py
```

If the video does not download successfully, its url will be retained and has to be fixed (via changing its file format etc.)
