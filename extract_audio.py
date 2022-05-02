
import subprocess
import os


def parse_audio():
    video_path  = "xx/"
    audio_path = "xx/"

    video_list = os.listdir(video_path)
    video_list.sort() 

    for i_video, name in enumerate(video_list): # len(video_list)
        cmd = "ffmpeg -y -i {} {}".format(video_path+name, audio_path+name[:-4] + '.wav')
        subprocess.call([cmd], shell=True)
        # tt

if __name__ == "__main__":
    parse_audio()