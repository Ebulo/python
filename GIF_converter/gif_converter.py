import imageio
import os
from pathlib import Path

path = Path()


def gifConverter(inpath, targetForm):
    outpath = os.path.splitext(clip)[0] + targetForm
    reader = imageio.get_reader(inpath)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(outpath, fps=fps)

    for frames in reader:
        writer.append_data(frames)
    print("Done!")
    writer.close()


# Add this script to a folder where the .mp4 files are to be converted to gif.
for i in path.glob("*.mp4"):
    clip = os.path.abspath(i)
    gifConverter(clip, ".gif")
