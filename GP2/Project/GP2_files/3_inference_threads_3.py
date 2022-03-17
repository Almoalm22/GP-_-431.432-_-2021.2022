import threading

import torch
import cv2
from threading import Thread
from datetime import datetime
import os
from IPython.display import Image

import torchvision.models as models

# =====================================================================================
def cam():
    src = 'rtsp://admin:GCKWAH@192.168.8.109/'
    camera = cv2.VideoCapture(src)
    i = 0
    while True:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        i += 1
        if i == 20:
            th = Thread(target=detect_img, args=(image,))
            th.daemon = True  # will be killed when the called thread finished its work
            th.start()
            i = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()


# =====================================================================================
def detect_img(img):
#lock
    global model
    i = datetime.now()
    i = str(i).replace(' ', '_')
    i = i.replace('-', '_')
    i = i.replace(':', '__')

    # i='x'

    cv2.imwrite('saved_imgs/' + i + '.jpg', img)
    img_scr = 'saved_imgs/' + i + '.jpg'
    results = model(img_scr)
    print('*********************************************')
    results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# release()



# =====================================================================================
if __name__ == '__main__':
    # model = torch.hub.load('yolov5-master/best_0.pt', 'yolov5l')  # or yolov5m, yolov5l, yolov5x, custom
    # path = r'E:\Emad_Files\Lab7\product_object_detection\yolov5\exp1\yolov5-master\runs\train\exp10\weights'

    # path=r"E:\Emad_Files\Lab7\product_object_detection\yolov5\exp1\yolov5-master"
    # model = torch.hub.load(path, source='local', model='yolov5l', pretrained=True)  # or yolov5m, yolov5l, yolov5x, custom
    model = torch.hub.load(r'C:\Users\moco_\Documents\Python\GP2\GP2_files',
                           'custom',
                           path=r'best.pt',
                           source='local')  # local repo
    cam()


from models.yolo import Model


# if __name__ == '__main__':
#     path = r'E:\Emad_Files\Lab7\product_object_detection\yolov5\exp1\yolov5-master\runs\train\exp10\weights'
#
#     model = Model(ch=3, nc=2, cfg='models/yolov5l.yaml')# we do not specify pretrained=True, i.e. do not load default weights
#     model.load_state_dict(torch.load('runs/train/exp10/weights/best.pt'))
#     model.eval()
#     cam()