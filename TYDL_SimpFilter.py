#import modules
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips #https://blog.devgenius.io/how-to-combine-an-audio-and-video-file-with-7-lines-of-python-a3e4d2d75c78
import os



yt = YouTube('https://www.youtube.com/watch?v=9bZkp7q19f0')
print(yt.title)




vStream=yt.streams.get_by_itag(137) #1080p without audio
aStream=yt.streams.get_by_itag(140) #Just the Audio

vStream.download()
aStream.download(filename=yt.title+'.mp3')



#Combine the video and Audio
title=(yt.title+'combined')

# Open the video and audio
video_clip = VideoFileClip(yt.title+'.mp4')
audio_clip = AudioFileClip(yt.title+'.mp3')

# Concatenate the video clip with the audio clip
final_clip = video_clip.set_audio(audio_clip)

# Export the final video with audio
final_clip.write_videofile(title + ".mp4")