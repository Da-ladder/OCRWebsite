from time import sleep
from .find import VideoAnalysis

imageProcessList = []
processingList = []
isActive = False
imageIsActive = False

class VideoProcesser:
    @staticmethod
    def main():
        global processingList, isActive
        isActive = True
        while (len(processingList) != 0):
            vid = processingList[0]
            VideoAnalysis.process_vid(vid)
            sleep(2)
            while (VideoAnalysis.getStat()[0] != -10):
               sleep(1)
            processingList.pop(0)
        
        isActive = False

    @staticmethod
    def addVideo(link):
        global processingList, isActive
        processingList.append(link)
        if not isActive:
           VideoProcesser.main()



class ImageProcesser:
    @staticmethod
    def main():
        global imageProcessList, imageIsActive
        imageIsActive = True
        index = 0
        while (len(imageProcessList) != 0):
            pass
        
        imageIsActive = False


    @staticmethod
    def findTeam(link, team):
        global imageProcessList, imageIsActive
        link = VideoAnalysis.yt_link_filter(link)
        if isinstance(team, list):
            imageProcessList.append([link, team])
        else:
            imageProcessList.append([link, [team]])
        
        if not imageIsActive:
           ImageProcesser.main()