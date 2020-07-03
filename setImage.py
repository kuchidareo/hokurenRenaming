import cv2
import datetime
import os
import numpy as np

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

date_today_str = datetime.date.today().strftime('%Y%m%d')

hokuren_dir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"+'\\hokuren'
h_today_dir = hokuren_dir + '\\' + date_today_str

mirror_dir = h_today_dir + '\\mirror'
pixel_dir = h_today_dir + '\\枝肉外観'
diffect_dir = h_today_dir + '\\瑕疵'

auction_dir = h_today_dir + '\\auction'

if(not os.path.exists(auction_dir)):
    os.mkdir(auction_dir)

ori_images = os.listdir(mirror_dir)
ori_port_images = os.listdir(pixel_dir)
ori_diffect_images = os.listdir(diffect_dir)

ori_port_images_list = []
print('mirror_image directory:' + mirror_dir)
print('pixel4_image directory:' + pixel_dir)
print('deffect_image directory:' + diffect_dir)
print('auction_image directory:' + auction_dir)
print("Proceccing...")

for i, ori_image in enumerate(ori_images):
    if "jpg" in ori_image or "JPG" in ori_image:
        buf = []
        for ori_port_image in ori_port_images:
            if ori_image[-8:-4] == ori_port_image[-10:-6]:
                buf.append(ori_port_image)
        for ori_diffect_image in ori_diffect_images:
            if ori_image[-8:-4] == ori_diffect_image[-10:-6]:
                buf.append(ori_diffect_image)
        if len(buf) > 3:
            img_0 = imread(mirror_dir +'\\'+ ori_image)
            img_0 = cv2.resize(img_0, dsize=(int(img_0.shape[1] / 4), int(img_0.shape[0] / 4)))
            img_0 = cv2.flip(img_0,0)
            img_1 = imread(pixel_dir +'\\'+ buf[0])
            img_2 = imread(pixel_dir +'\\'+ buf[1])
            img_3 = imread(pixel_dir +'\\'+ buf[2])
            img_4 = imread(pixel_dir +'\\'+ buf[3])
            if len(buf) > 4:
                img_5 = imread(diffect_dir +'\\'+ buf[4])
                img_0[img_0.shape[0]-800:img_0.shape[0], img_0.shape[1]-600:img_0.shape[1]] = cv2.resize(img_5, dsize=(600, 800))
            cv2.putText(img_0, str(ori_image[-12:-4]), (10, 300), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 7.0, (0, 255, 255), thickness=20)
            tile_img = cv2.hconcat([cv2.vconcat([img_1,img_2]),cv2.vconcat([img_3,img_4])])
            resize_width = int(tile_img.shape[1] * img_0.shape[0] / tile_img.shape[0])
            resize_height = int(img_0.shape[0])
            tile_img = cv2.resize(tile_img, dsize=(resize_width,resize_height))
            img = cv2.hconcat([img_0, tile_img])
            cv2.imwrite(auction_dir + '\\a' + ori_image[-12:], img)
        else:
            print("----------------------------")
            print("error at:" + ori_image[-12:-4])
            print("----------------------------")
    print(str(i+1)+'/'+str(len(ori_images)))
