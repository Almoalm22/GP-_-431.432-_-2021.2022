import torch, cv2, mysql.connector
from playsound import playsound

# =====================================================================================

def cam():
    src = 0  # 'rtsp://admin:GCKWAH@192.168.8.109/' # put 0 for web cam
    camera = cv2.VideoCapture(src)
    i = 0
    while True:
        return_value, image = camera.read()
        cv2.imshow('image', image)
        results = model(image)
        results.xyxy[0]
        x = results.pandas().xyxy[0]  # or .show(), .save(), .crop(), .pandas(), etc.
        rows = x.shape[0]
        cols = x.shape[1]

        for i in range(rows):

            ob_class = str(x.iat[i, cols - 2])
            ob_name = str(x.iat[i, cols - 1])
            ob_conf = str(x.iat[i, cols - 3])
            x1 = int(x.iat[i, cols - 7])
            y1 = int(x.iat[i, cols - 6])
            x2 = int(x.iat[i, cols - 5])
            y2 = int(x.iat[i, cols - 4])

            start_point = (x1, y1)  # represents the top left corner of rectangle
            end_point = (x2, y2)  # represents the bottom right corner of rectangle
            if int(ob_class) == 0:
                color = (180, 0, 0)  # Blue color in BGR
            elif int(ob_class) == 1:
                color = (0, 0, 180)  # Red color in BGR
            thickness = 2  # Line thickness of 2 px

            label = (ob_name.title() + " " + "{:.2%}".format(float(ob_conf)))

            # Draw a rectangle with blue line borders of thickness of 2 px
            image = cv2.rectangle(image, start_point, end_point, color, thickness)

            # For the text background
            # Finds space required by the text so that we can put a background with that amount of width.
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

            # Prints the text.
            img = cv2.rectangle(image, (x1, y1 - 20), (x1 + w, y1), color, -1)
            img = cv2.putText(image, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

            # For printing text
            img = cv2.putText(image, label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow('image', image)

            if float(ob_conf) > 0.6:
                playsound('Police.mp3')

                # if int(ob_class) == 0:
                #     playsound('knife.mp3')
                # elif int(ob_class) == 1:
                #     playsound('gun.mp3')

            print(ob_class, ob_name, ob_conf)
            store_DB(ob_class, ob_name, ob_conf)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

def store_DB(ob_class, ob_name, ob_conf):
    sql = mysql.connector.connect(host="localhost", user="root", password="2525", database="wd_cctv",
                                  auth_plugin='mysql_native_password')
    cur = sql.cursor()
    cur.execute("INSERT into object values(null,%s,%s,%s,CURRENT_DATE(),CURRENT_TIME)", (ob_class, ob_name, ob_conf))
    sql.commit()
    return

def main():
    global model
    model = torch.hub.load(r'C:\Users\moco_\Documents\Python\GP2\GP2_files',
                           'custom',
                           path=r'best.pt',
                           source='local')  # local repo
    cam()


# =====================================================================================
# conn = None
if __name__ == '__main__':
    main()
