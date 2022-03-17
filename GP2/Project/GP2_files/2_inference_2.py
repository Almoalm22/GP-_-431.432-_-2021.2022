import os

# os.system("python detect.py --weights v61_yolov5x6.pt --img 640 --conf 0.6 --source data\\images")

os.system("python detect.py --weights best.pt --img 640 --conf 0.5 --source data\\test")

