# read video url from videos.txt and get video's channel name using yt-dlp
from yt_dlp import YoutubeDL, postprocessor
import json
import os
import subprocess
import sys


def progress_hook(d):
    # if d["status"] == "downloading":
    # sys.stdout.write(
    #     "\rDownloading: %s [%s] ETA %s"
    #     % (d["_percent_str"], d["_speed_str"], d["_eta_str"])
    # )
    # sys.stdout.flush()
    # pass
    if d["status"] == "finished":
        print("\nDownload completed successfully!\n")


ydl_opts = {
    "ignoreerrors": False,
    "format": "22",
    "break_on_reject": True,
    "lazy_playlist": True,
    "quiet": True,
    "no_warnings": True,
    "writedescription": True,
    "downloader": "aria2c",
    "downloader_args": 'aria2c:"-s 4 -x 4 -j 4"',
    "progress": True,
    "progress_template": {
        "download": " %(info.original_url)s - %(progress._percent_str)s of %(progress._total_bytes_str)s @ %(progress._speed_str)s - ETA: %(progress._eta_str)s",
    },
    "progress_hooks": [progress_hook],
    "postprocessors": [
        {
            "actions": [
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    "&",
                    "and",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    "\\!",
                    "",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    ":",
                    " -",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    "\\|",
                    "-",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    "\\'",
                    "",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    "\\?",
                    "",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    "\\/",
                    "-",
                ),
                (
                    postprocessor.metadataparser.MetadataParserPP.replacer,
                    "title",
                    '"',
                    "",
                ),
            ],
            "key": "MetadataParser",
            "when": "pre_process",
        },
        {"key": "FFmpegConcat", "only_multi_video": True, "when": "playlist"},
    ],
}


with open("chanpath.json", "r") as file:
    chan_path = json.load(file)
ERROR = None
line_to_keep = []
ydl = YoutubeDL(ydl_opts)
with open("videos.txt", "r") as f:
    for line in f:
        video_url = line.strip()
        print(f"Downloading video: {video_url}")
        info = ydl.extract_info(video_url, download=False)
        channel_name = info["channel"].replace(" ", "")
        # print(f"{video_url} is from channel {channel_name}")
        available_formats = [f["format_id"] for f in info["formats"]]
        # check if format 22 is available
        if "22" in available_formats:
            # print(f"{video_url} is available in format 22")
            path = chan_path[channel_name]

            print(f"Downloading video: {video_url} to {path}")

            # download using ydl.download and specify path
            dest = path + "/%(upload_date)s - %(title)s.%(ext)s"
            ydl.params["outtmpl"]["default"] = dest

            try:
                ydl.download([video_url])
                print(f"Video downloaded to {path}")
                print("")

            except Exception as e:
                print(f"Download failed: {e}")
                ERROR = True
                line_to_keep.append(video_url)
            finally:
                continue

        else:
            ERROR = True
            print(f"{video_url} is not available in format 22")

# keep all lines in line_to_keep in videos.txt
with open("videos.txt", "w") as file:
    file.write("\n".join(line_to_keep))

if ERROR:
    print("Error: Some videos could not be downloaded")
    subprocess.run(
        [
            "notify-send",
            "--urgency=low",
            "-i",
            "dialog-warning",
            "Some videos could not be downloaded",
        ],
        capture_output=True,
        text=True,
    )
else:
    print("All videos downloaded")
    subprocess.run(
        [
            "notify-send",
            "--urgency=low",
            "-i",
            "emblem-ok",
            "All videos downloaded",
        ],
        capture_output=True,
        text=True,
    )
