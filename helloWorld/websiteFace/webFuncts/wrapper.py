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

    @staticmethod
    def checkList(link):
        global processingList
        for url in processingList:
            if url == link:
                return True
        return False



class ImageProcesser:
    @staticmethod
    def main():
        global imageProcessList, imageIsActive
        imageIsActive = True
        index = 0
        while (len(imageProcessList) != 0):
            if (VideoAnalysis.checkVidStorage(imageProcessList[index][0])):
                print("hyay")
                VideoAnalysis.find_team(imageProcessList[index][0], imageProcessList[index][1]) # passes a list to the second param
                imageProcessList.pop(index)
                # TODO figure out how to spit back found matches for each team
            else:
                print("roip")
                if (not VideoProcesser.checkList(imageProcessList[index][0])):
                    print(imageProcessList[index][0])
                    VideoProcesser.addVideo(imageProcessList[index][0])
                if (len(imageProcessList)-1) > index:
                    index += 1
                else:
                    index = 0
                sleep(1) # wait one second before checking the list again
        
        imageIsActive = False


    @staticmethod
    def findTeam(link, team):
        global imageProcessList, imageIsActive
        #link = VideoAnalysis.yt_link_filter(link)
        if isinstance(team, list):
            imageProcessList.append([link, team])
        else:
            imageProcessList.append([link, [team]])
        
        if not imageIsActive:
            ImageProcesser.main()