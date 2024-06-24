from time import sleep
from .find import VideoAnalysis
from ..models import VideoStorage


imageProcessList = []
processingList = []
isActive = False
imageIsActive = False

class VideoProcesser:
    @staticmethod
    def main():
        global processingList, isActive
        isActive = True # lets other methods check progress

        # loop is active while videos still exist to process
        while (len(processingList) != 0):
            vid = processingList[0]
            VideoAnalysis.process_vid(vid) # stalls here while video is processing
            processingList.pop(0) # removes video as it has been processed
        
        isActive = False

    @staticmethod
    def addVideo(link):
        global processingList, isActive

        # checks if video is in queue. Checks for processed videos will come later
        if (not VideoProcesser.checkList(link)):
            processingList.append(link)

        # activate main loop if it is not active
        if not isActive:
           VideoProcesser.main()

    @staticmethod
    def checkList(link):
        
        global processingList

        # goes through current queue to check if the video is to be processed
        for url in processingList:
            if url == link:
                return True
        return False
    
    @staticmethod
    def giveProcessList():
        # returns whatever is in processing list currently
        global processingList
        return processingList



class ImageProcesser:
    @staticmethod
    def main():
        global imageProcessList, imageIsActive
        imageIsActive = True
        index = 0
        print("is worky?")
        while (len(imageProcessList) != 0):
            # checks if the video has already been found
            if (VideoAnalysis.checkVidStorage(imageProcessList[index][0])):
                # finds team through extracted video information
                VideoAnalysis.find_team(imageProcessList[index][0], imageProcessList[index][1])
                imageProcessList.pop(index)
                # TODO figure out how to spit back found matches for each team
            else:
                if (not VideoProcesser.checkList(imageProcessList[index][0])):
                    print("link = " + imageProcessList[index][0]) # prints out link
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

        # formats link & team together 
        if isinstance(team, list):
            linkTeam = [link, team]
        else:
            linkTeam = [link, [team]]
        
        # adds video to the processing list if it is not in processing list
        if not ImageProcesser.checkList(linkTeam):
            imageProcessList.append(linkTeam)
        
        # activate main loop if it is not active
        if not imageIsActive:
            ImageProcesser.main()

    @staticmethod
    def checkList(item):
        global imageProcessList

        for i in processingList:
            if i == item:
                return True
        return False

