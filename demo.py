import os
import cv2
import numpy as np
import imageio

video_path = "xx/mvva_video/"
hmap_path = "xx/save_our_hmap/"
save_hmap_video = "xx/hmap_video/"

def visualize_hmap():
    video_list = os.listdir(video_path)
    for i, name in enumerate(video_list):
        
        # if not name[:-4] in ['005', '008', '040', '058', '082', '155', '189']:
        if not name[:-4] in ['82']:
            continue

        ## read all imgs
        all_frames = []
        cap = cv2.VideoCapture(video_path + name)

        count = 0
        while (1):
            ret, frame = cap.read()
            # cv2.imshow("capture", frame)  # 显示视频帧
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if ret:
                all_frames.append(frame)
                count += 1
                print(">>>> count: ", count)
            else:
                break

        ## read all hmaps
        all_hmaps = []
        hmap_path1 = hmap_path + "video_%03d"%(int(name[:-4]))
        hmap_list = os.listdir(hmap_path1)
        for i_frame in range(len(hmap_path1)):
            read_hmap = hmap_path1 + '/%03d.jpg'%i_frame
            all_hmaps.append(cv2.imread(read_hmap, 0))
        
        print(">>>> len(all_frames): ", len(all_frames), len(all_hmaps))

        writer = imageio.get_writer(save_hmap_video + '/{}.mp4'.format(name[:-4]), fps=25)
        for i_frame, pair in enumerate(zip(all_frames, all_hmaps)):
            img, hmap = pair[0], pair[1]
            h, w, _ = np.shape(img)
            hmap = cv2.resize(hmap, (w, h))

            print(">>>> len(all_frames): ", np.shape(img), np.shape(hmap))

            heat_img = cv2.applyColorMap(hmap, cv2.COLORMAP_JET)
            # heat_img = cv2.cvtColor(mask_map, cv2.COLOR_BGR2RGB)

            img_add = cv2.addWeighted(img, 0.6, heat_img, 0.4, 0)
            img_ad = cv2.cvtColor(img_add, cv2.COLOR_BGR2RGB)
            writer.append_data(img_ad)
            # cv2.imwrite(save_hmap_video+'1.jpg', img_add)
            # tt
        writer.close()
        # tt

if __name__ == "__main__":
    visualize_hmap()