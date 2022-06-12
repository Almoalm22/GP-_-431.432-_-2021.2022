import sqlite3

import torch
import cv2

# =====================================================================================
'''check this
https://www.forecr.io/blogs/ai-algorithms/how-to-run-yolov5-real-time-object-detection-on-nvidia%C2%AE-jetson%E2%84%A2-nano%E2%84%A2
https://www.section.io/engineering-education/object-detection-with-yolov5-and-pytorch/#model-inference-using-detectpy
'''


def cam():

    src = 'rtsp://admin:GCKWAH@192.168.8.109/'  # put 0 for web cam
    camera = cv2.VideoCapture(src)
    i = 0
    while True:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        results = model(image)
        x = results.pandas().xyxy[0]  # or .show(), .save(), .crop(), .pandas(), etc.
        rows = x.shape[0]
        cols = x.shape[1]
        for i in range(rows):
            print(x.iat[i, cols - 1])
            store_DB(x.iat[i, cols - 1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()


def create_connection(db_file):
    c = None
    try:
        c = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return c


def store_DB(obj):
    sql = ''' INSERT INTO objects (name) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (obj,))
    conn.commit()


def main():
    global conn
    conn = create_connection('db.db')
    global model
    model = torch.hub.load(r'D:\Emad_Files\GP2_432\GP2_ver3_training',
                           'custom',
                           path=r'yolov5s6.pt',
                           source='local')  # local repo

    cam()


# =====================================================================================
# conn = None
if __name__ == '__main__':
    main()