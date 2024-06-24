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

from .FrameCapture import Video2Images
from .timer import Timer
from ..models import VideoStorage

currStat = 0
downloadPercentage = 0
frameCaptureStatus = 30
analysisStatus = 0

# Gets filepath two levels up from the current directory with the following folder names. MAKE FOLDERS IF THEY DO NOT EXIST 
# TODO change to new filesystem!!! (will still require folders)
vid_storage = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "videos")
image_storage = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "images")
team_results = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "results")
vid_track = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "Videolist.txt")


class VideoAnalysis:
    @staticmethod
    def getStat():
        global currStat, downloadPercentage, frameCaptureStatus, analysisStatus

        #returns the stage of processing the video is in
        if currStat == 0:
            return [-10, 0]
        else:
            if currStat == 1:
                return [currStat, downloadPercentage]
            elif currStat == 2:
                return [currStat, frameCaptureStatus]
            elif currStat == 3:
                return [currStat, analysisStatus]


    @staticmethod
    def yt_link_filter(yt_link):
        # filter links so that only video key remains
        if (yt_link.find("&t") == -1):
            pass
        else:
            yt_link = yt_link[:yt_link.find("&t")]
        if (yt_link.find("v=") == -1):
            pass
        else:
            yt_link = yt_link[yt_link.find("v=")+2:]
        return yt_link


    @staticmethod
    def progressBar(count_value, total, suffix=""):
        global downloadPercentage
        # Makes a visual bar (in command line) for devs to see progress
        bar_length = 100
        filled_up_Length = int(round(bar_length * count_value / float(total)))
        percentage = round(100.0 * count_value / float(total), 1)
        downloadPercentage = percentage
        bar = "=" * filled_up_Length + "-" * (bar_length - filled_up_Length)
        #os.system("cls") # clears bar but no need
        print("[%s] %s%s ...%s" % (bar, percentage, "%", suffix))
        sys.stdout.write("\033[F")
        sys.stdout.flush()


    @staticmethod
    def on_progress(stream, chunk, bytes_remaining):
        # updates the bar
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        VideoAnalysis.progressBar(bytes_downloaded, total_size)


    @staticmethod
    def down_yt_vid(yt_link, yt_fold_name, itag=None):
        global vid_storage, currStat, downloadPercentage, frameCaptureStatus, analysisStatus

        # starts the timer and changes the stage of processing it is on
        currStat = 1
        tracker = Timer()

        # creates an object so that the video can be installed
        video = YT(
            yt_link,
            on_progress_callback=VideoAnalysis.on_progress,
            use_oauth=True,
            allow_oauth_cache=True,
        )

        # try block to catch download errors
        try:
            if itag is None:
                stream = video.streams.get_highest_resolution()
            else:
                stream = video.streams.get_by_itag(itag)  # 136 = 720p 134 = 360p
            stream.download(
                output_path=vid_storage, filename=(yt_fold_name + ".mp4")
            )
            print("your video downloaded successfully")

            # Makes a new data entry into the database if download is successful
            vid = VideoStorage(
                vid_name = video.title,
                vid_sec_length = video.length,
                vid_key = yt_fold_name,
                vid_extracted = ""
            )
            vid.save()
        except AttributeError:
            print("failed to download in {:} itag".format(itag))
        else:
            print("failed?")
        print(tracker.end_time())


    @staticmethod
    def split_frames(ytlink):
        global image_storage, currStat, downloadPercentage, frameCaptureStatus, analysisStatus

        # changes the stage of processing it is on and starts timer
        currStat = 2
        tracker = Timer()

        vid_loc = os.path.join(vid_storage, ytlink) + ".mp4"
        frameCaptureStatus = 9 # TODO make frame capture update more accurate
        Video2Images(
            video_filepath=vid_loc,
            out_folder_name=ytlink,
            capture_rate=0.0165,
            out_dir=image_storage,
        )
        frameCaptureStatus = 99.9
        print(tracker.end_time())


    @staticmethod
    def frame_read(ytlink):
        global team_results, currStat, downloadPercentage, frameCaptureStatus, analysisStatus

        # changes the stage of processing it is on and starts timer
        currStat = 3
        tracker = Timer()

        # sets up easy OCR & the location of the captured frames
        reader = easyocr.Reader(["en"], gpu=True)
        frame_loc = os.path.join(image_storage, ytlink)

        # counts the number of captured frames in the folder
        numOfFiles = 0
        for filename in os.listdir(frame_loc):
            numOfFiles += 1

        # sets up appendText and tracks current frame in processing
        appendText = ""
        curNum = 0

        for filename in os.listdir(frame_loc):
            # increments current frame and reads it
            curNum += 1
            result = reader.readtext(os.path.join(frame_loc, filename), detail=0)

            # updates the progress percentage and adds the output to appendText
            analysisStatus = (curNum/numOfFiles)*100
            appendText += "Output: " + str(result) + " file: " + str(filename) + "\n"

        # grabs video instance, adds extracted text, and saves it
        vidInstance = VideoStorage.objects.get(vid_key=ytlink)
        vidInstance.vid_extracted = appendText
        vidInstance.save()

        print(tracker.end_time)


    @staticmethod
    def urlgen(yt_link, filename):
        filename = filename.removesuffix(".jpg")  # filename can not be a path

        # generates a link to the exact timestamp in the video
        final_link = yt_link + "&t={:}s".format(filename)

        return final_link


    @staticmethod
    def find_team(yt_link, team):
        filteredLink = VideoAnalysis.yt_link_filter(yt_link)
        foundMatches = []
        with open(
            os.path.join(team_results, filteredLink + ".txt"), "r"
        ) as file:
            for line in file:
                line = line.removeprefix("Output: ")
                file_timestamp = line[line.find("file: ") + 6 : -5]
                line = line[: line.find(" file:")]
                line = line.replace("'", "").removesuffix("]").removeprefix("[")
                line = line.split(", ")
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
                        for targetTeam in team:
                            if targetTeam == teams:
                                foundMatches.append(targetTeam)
                                link = "https://www.youtube.com/watch?v=" + filteredLink + "&t=" + str(file_timestamp) + "s"
                                foundMatches.append(link)
                                print(targetTeam, "FOUND AT", link)
        
        return foundMatches


    @staticmethod
    def process_vid(yt_link, team=None):
        global currStat, downloadPercentage, frameCaptureStatus, analysisStatus
        start_time = time.time()
        yt_folder_name = VideoAnalysis.yt_link_filter(yt_link)
        print(yt_folder_name)
        print("The name for the yt video is:", yt_folder_name)
        if VideoAnalysis.checkVidStorage(yt_folder_name):
            print("Video Already Processed!")
        else:
            VideoAnalysis.down_yt_vid(yt_link, yt_folder_name)
            VideoAnalysis.split_frames(yt_folder_name)
            VideoAnalysis.frame_read(yt_folder_name)
        print((time.time() - start_time))

        # add video to processed list
        with open(vid_track, 'a') as file:
            file.write(yt_folder_name + "\n")
        # end of appendings



        # resets all stats so that the next video can be processed
        currStat = 0
        downloadPercentage = 0
        frameCaptureStatus = 0
        analysisStatus = 0


    @staticmethod
    def checkVidStorage(ytlink):
        filteredLink = VideoAnalysis.yt_link_filter(ytlink)
        with open(vid_track, 'r') as file:
            for line in file:
                if (line.strip("\n") == filteredLink):
                    return True

        return False



start_time = time.time()



"""
yt_link = "https://www.youtube.com/watch?v=uCrFhEUjyLY&t=21099s"
yt_folder_name = yt_link_filter(yt_link)
print(yt_folder_name)
#down_yt_vid(yt_link, yt_folder_name)
split_frames(yt_folder_name)
frame_read(yt_folder_name)
"""

