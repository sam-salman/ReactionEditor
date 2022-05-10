import moviepy
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx
import os
import sys
import time
import numpy as py
import logging as log


# create a log file to store logs of the app
log.basicConfig(
    filename="logs.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=log.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def editor(paths):
    # get the title of the viddeo from the basename
    try:
        title = os.path.basename(paths['video']).split('.')[0]
        print("title: ", title)
    except Exception as e:
        log.error("Error in setting title: ", e)
        print("An error occured" + str(e))
        print("setting title as default: output")
        title = "output"

        
    
    try:
        video = VideoFileClip(paths['video'])
        videoDuration = video.duration

        reaction = VideoFileClip(paths['reaction']).resize(0.2).volumex(0)
        reactionDuration = reaction.duration
        print("Duration of Video: " + str(videoDuration))
        print("Duration of Reaction: " + str(videoDuration))
        log.info("Video and reaction paths are set succefully")

    except Exception as e:
        log.error("An error occured in assigning videos" + str(e))



    try:
        if videoDuration > reactionDuration:
            difference = videoDuration -  reactionDuration


            while videoDuration > reactionDuration:
                newClip = reaction.subclip(0, reactionDuration)
                reaction = concatenate_videoclips([newClip, reaction])
                reactionDuration = reaction.duration
                difference = videoDuration -  reactionDuration

            reaction = reaction.set_duration(videoDuration)
            reactionDuration = reaction.duration
            log.info("Reaction and video duration are matched" + str(reactionDuration) + " " + str(videoDuration))    
        elif videoDuration < reactionDuration:
            reaction = reaction.subclip(0, videoDuration)
            reactionDuration = reaction.duration
            log.info("Reaction and video duration are matched" + str(reactionDuration) + " " + str(videoDuration))

    except  Exception as e:
        log.error("An error occured matching durations" + str(e))
        print("An error occured matching durations" + str(e))

    print("Duration of video: " + str(videoDuration))
    print("Duration of reaction: " + str(reactionDuration))   

    try:
        final_clip = CompositeVideoClip([video, reaction.set_position(("right","top"))])
        log.info("Video and reaction are composited")
        # write video file at the provide path

        final_clip.write_videofile(title + ".mp4")
        log.info("Video is written successfully")
        print("Video Created")
        return 
        # self.proc.terminate()
    except Exception as e:
        log.error("An error occured in compositing or creating video" + str(e))
        print("Error" + str(e))

        



print("Welcome to the Video Editor")
print("Please enter the path to the video you want to edit")
video = input()
print("Please enter the path to the reaction you want to add")
reaction = input()
paths = {'video': video, 'reaction': reaction}
editor(paths)
sys.exit(0)