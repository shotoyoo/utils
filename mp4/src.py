from moviepy.editor import VideoFileClip
import sys
import os
import pdb
from pathlib import Path

def divide(fname, start, end):
    video = VideoFileClip(os.path.join("./in",fname))
    video = video.subclip(start, end)
    video.write_videofile(os.path.join("./out/", fname))

if __name__=="__main__":
    path, start, end = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    fname = Path(path).name
    divide(fname, start, end)