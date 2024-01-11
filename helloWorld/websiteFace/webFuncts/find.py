from __future__ import unicode_literals

import os
import random
import sys
import time

# import numpy as np
# import torch

# import cv2
import easyocr.easyocr

# from cv2 import dnn_superres
from pytube import YouTube as YT

#import frameCapture
from .timer import Timer


start_time = time.time()
vid_storage = os.path.join(os.getcwd(), "videos")
image_storage = os.path.join(os.getcwd(), "images")
team_results = os.path.join(os.getcwd(), "results")


def yt_link_filter(yt_link):
    yt_link = yt_link[
        : yt_link.find("&t")
    ]  # filter links before doing anything else to ensure consistency
    yt_link = yt_link[yt_link.find("v=") + 2 :]
    return yt_link


def progressBar(count_value, total, suffix=""):
    bar_length = 100
    filled_up_Length = int(round(bar_length * count_value / float(total)))
    percentage = round(100.0 * count_value / float(total), 1)
    bar = "=" * filled_up_Length + "-" * (bar_length - filled_up_Length)
    os.system("cls")
    print("[%s] %s%s ...%s" % (bar, percentage, "%", suffix))
    sys.stdout.write("\033[F")
    sys.stdout.flush()


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progressBar(bytes_downloaded, total_size)


def down_yt_vid(yt_link, yt_fold_name, itag=None):
    tracker = Timer()

    video = YT(
        yt_link,
        on_progress_callback=on_progress,
        use_oauth=True,
        allow_oauth_cache=True,
    )
    try:
        if itag is None:
            stream = video.streams.get_highest_resolution()
        else:
            stream = video.streams.get_by_itag(itag)  # 136 = 720p 134 = 360p
        stream.download(
            output_path=vid_storage
        )  #''', filename=(yt_fold_name + ".m4a")'''
        print("your video downloaded successfully")
    except AttributeError:
        print("failed to download in {:} itag".format(itag))
    else:
        print("done")
    print(tracker.end_time())


down_yt_vid("https://www.youtube.com/watch?v=5tFmpn_y-s0", "personal", 140)


def split_frames(ytlink):
    vid_loc = os.path.join(vid_storage, ytlink) + ".mp4"
    tracker = Timer()
    frameCapture.Video2Images(
        video_filepath=vid_loc,
        out_folder_name=ytlink,
        capture_rate=0.0165,
        out_dir=image_storage,
    )
    print(tracker.end_time())


def frame_read(ytlink):
    tracker = Timer()
    reader = easyocr.Reader(["en"], gpu=True)
    os_path = os.path.join(team_results, ytlink)
    text_file = open(os_path, "w")
    frame_loc = os.path.join(image_storage, ytlink)

    list_o_frame = []
    num = 0
    for filename in os.listdir(frame_loc):
        # list_o_frame.append(os.path.join(framls, filename))
        result = reader.readtext(os.path.join(frame_loc, filename), detail=0)
        print(os.path.join(image_storage, filename))
        print(result)
        text_file.write("Output: " + str(result) + " file: " + str(filename) + "\n")

    text_file.close()
    print(tracker.end_time)


# removes .jpg from th end of the file - tags on the youtube name and the file name
def urlgen(yt_link, filename):
    filename = filename.removesuffix(".jpg")  # filename can not be a path
    final_link = yt_link + "&t={:}s".format(filename)

    return final_link


# most computational part of the program
def process_vid(yt_link):
    yt_folder_name = yt_link_filter(yt_link)
    print("The name for the yt video is:", yt_folder_name)
    down_yt_vid(yt_link, yt_folder_name)
    split_frames(yt_folder_name)
    frame_read(yt_folder_name)


# Hi test
def find_team(yt_link, team):
    with open(
        r"C:\Users\zcody\PycharmProjects\keras-test\results\sCpLBEfHb8.txt", "r"
    ) as file:
        for line in file:
            line = line.removeprefix("Output: ")
            file_timestamp = line[line.find("file: ") + 6 : -5]
            line = line[: line.find(" file:")]
            line = line.replace("'", "").removesuffix("]").removeprefix("[")
            line = line.split(", ")
            #
            extraneous_matches = False
            for item in line:
                item = item.strip()
                if (
                    item.lower() == "elimination bracket"
                    or item.lower().find("alliance selection") != -1
                ):
                    # print("emlim bracket")
                    extraneous_matches = True
                    break
                elif item.lower() == "qualification rankings" or item.lower() == (
                    "wp" and "ap"
                ):
                    # print("qual rankings")
                    extraneous_matches = True
                    break
                elif (
                    item.lower() == "rank"
                    or item.lower() == "match schedule"
                    or item.lower() == "red teams"
                ):
                    # print("ranks")
                    extraneous_matches = True
                    break

            if not extraneous_matches:
                for teams in line:
                    if teams == team:
                        print(team, "found at", file_timestamp)
                        break


# process_vid("https://www.youtube.com/watch?v=sCpLBEfHb88")
# trying to fuck around with running open AI model on gpu using cuda 11.7 toolkit may need to reinstall torch 117
# find_team("", "8878D")

"""
yt_link = "https://www.youtube.com/watch?v=uCrFhEUjyLY&t=21099s"
yt_folder_name = yt_link_filter(yt_link)
print(yt_folder_name)
#down_yt_vid(yt_link, yt_folder_name)
split_frames(yt_folder_name)
frame_read(yt_folder_name)
"""

# wow = reader.readtext_batched(list_o_frame, detail=0)
# print(wow)
print((time.time() - start_time))
