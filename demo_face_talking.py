
import os
import imageio
import time
from tqdm import trange, tqdm
import xlrd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import subprocess

def plot_mouth_data_one_hmap_image_new_labeld(one_video_frames, one_video_face_ID_data, one_video_mouth_data,
    save_demo_video_path, name, fps):
    blue = (255, 0, 0)
    red = (0, 0, 255)
    green = (0, 255, 0)
    font = cv2.FONT_HERSHEY_COMPLEX

    valid_frame = np.min([np.shape(one_video_frames)[0], np.shape(one_video_face_ID_data)[0], 
                          np.shape(one_video_mouth_data)[1]])

    writer = imageio.get_writer(save_demo_video_path, fps=fps)

    for i_frame in trange(valid_frame):
        one_frame_image = one_video_frames[i_frame]
        one_frame_talking_data = one_video_mouth_data[:, i_frame]
        one_frame_face_tracking_data = one_video_face_ID_data[i_frame]

        num_face = len(one_frame_face_tracking_data)
        for i_face in range(num_face):
            
            one_face_data = one_frame_face_tracking_data[i_face] 
            x1, y1, x2, y2 = int(one_face_data[0]), int(one_face_data[1]),  int(one_face_data[2]),  int(one_face_data[3]),  

            line_width = 2; box_color = blue; text_color = green

            if int(one_frame_talking_data[i_face]) == 1:
                # print(">>>>> enter here", one_frame_talking_data[talking_face_ID])
                line_width = 4; box_color = red; text_color = red
            
            cv2.rectangle(one_frame_image, (x1, y1), (x2, y2), box_color, line_width)
            cv2.putText(one_frame_image, "ID: %d"%(i_face+1), (x1, y1), font, 1, text_color)

        # cv2.imshow("1", one_frame_image)
        # cv2.waitKey() 
        writer.append_data(cv2.cvtColor(one_frame_image, cv2.COLOR_BGR2RGB))

    writer.close()

def load_one_video_frames(video_path):
    start_time = time.time()

    one_video_frames = []
    cap = cv2.VideoCapture(video_path)
    fps=cap.get(cv2.CAP_PROP_FPS)

    if not cap.isOpened():
        print("Cannot open video")
        exit()
    
    while True:
        ret, frame = cap.read()
        if len(np.shape(frame)) <= 1:
            pass
        else:
            one_video_frames.append(frame)
        if not ret: 
            print("Can't receive frame (stream end?). Exiting ...")
            break
    cap.release() 
    
    print('>>>> load video: {} {} images, time: {} s'.format(
          video_path.split('/')[-1], len(one_video_frames), time.time()-start_time))

    return one_video_frames, fps

def plot_face_talking_tracking():
    video_path = "xx/"
    audio_path = "xx/"
    face_tracking_path = "xx/" # 
    face_talking_path = "xx/"
    save_demo_video_path = "xx/"

    video_list = os.listdir(video_path)
    video_list.sort()

    pbar = tqdm(total=len(video_list))
    for i_video, name in enumerate(video_list): # len(video_list)
        pbar.update(1)
        print("{}\t{}".format(i_video, name))

        if not name[:-4] in ["91"]: # for talking
            continue
        
        one_video_frames, fps = load_one_video_frames(video_path + name)
        tracking_data = np.load(face_tracking_path + name[:-4] + ".npy")
        talking_data = np.load(face_talking_path + name[:-4] + ".npy")

        # print("{}\t{}".format(name, np.shape(tracking_data)))
        # print("{}\t{}".format(name, np.shape(talking_data)))

        save_demo_video_path1 = save_demo_video_path + name[:-4] + "_wo_audio.avi"
        plot_mouth_data_one_hmap_image_new_labeld(one_video_frames, tracking_data, talking_data,
                                                  save_demo_video_path1, name, fps)

        read_audio_path = audio_path + name[:-4] + ".wav"
        save_ID_audio_video_path = save_demo_video_path + name[:-4] + "_wt_audio.avi"
        command = "ffmpeg -y -i {} -i {} -c:v copy -c:a aac {}".format(save_demo_video_path1, 
                   read_audio_path, save_ID_audio_video_path)
        print(">>>>> pro_video_046: ", command)

        subprocess.call([command], shell=True) 
    
    pbar.close()
    
    time.sleep(10)
    cmd1 = 'rm -rf {}/*_wo_audio.avi'.format(save_demo_video_path)
    subprocess.call([cmd1], shell=True)


if __name__ == "__main__":
    plot_face_talking_tracking()