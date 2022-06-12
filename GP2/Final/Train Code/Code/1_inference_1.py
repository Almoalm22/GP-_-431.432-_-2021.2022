import torch

# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, custom
model = torch.hub.load(r'C:\Users\moco_\Documents\Python\GP2\GP2_files',
                           'custom',
                           path=r'best.pt',
                           source='local')  # local repo
# Images

path=r'C:\Users\moco_\Documents\Python\GP2\GP2_files\data\images\Pistol (102).jpg'
# path=r'D:\Emad_Files\GP2_432\GP2_ver3_training\data\images\bus.jpg'
img = path  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.