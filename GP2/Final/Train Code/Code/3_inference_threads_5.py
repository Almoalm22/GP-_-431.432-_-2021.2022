import torch
import cv2
from threading import Thread
from datetime import datetime
import detect
# =====================================================================================
def cam():
    src = 'rtsp://admin:GCKWAH@192.168.8.109/' # put 0 for web cam
    camera = cv2.VideoCapture(src)
    i = 0
    while True:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        i += 1
        if i == 50:
            th = Thread(target=detect_img2, args=(image,))
            th.daemon = True  # will be killed when the called thread finished its work
            th.start()
            i = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
# =====================================================================================
def detect_img2(img):
    global model
    results = model(img)
    # results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
    # results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
    # results.pandas()  # or .show(), .save(), .crop(), .pandas(), etc.
    x=results.pandas().xyxy[0] # or .show(), .save(), .crop(), .pandas(), etc.
    # print(x)
    rows= x.shape[0]
    cols= x.shape[1]
    for i in range(rows):
        print(x.iat[i,cols-1])


def detect_img1(img):
    global model
    i = datetime.now()
    i = str(i).replace(' ', '_')
    i = i.replace('-', '_')
    i = i.replace(':', '__')
    cv2.imwrite('saved_imgs/' + i + '.jpg', img)
    img_scr = 'saved_imgs/' + i + '.jpg'
    results = model(img_scr)
    results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

# =====================================================================================
if __name__ == '__main__':
    model = torch.hub.load(r'C:\Users\moco_\Documents\Python\GP2\GP2_files',
                           'custom',
                           path=r'best.pt',
                           source='local')  # local repo

    th1=Thread(target=cam)
    th1.start()
