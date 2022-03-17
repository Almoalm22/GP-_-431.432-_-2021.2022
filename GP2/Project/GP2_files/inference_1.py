import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x')  # or yolov5m, yolov5l, yolov5x, custom
# model = torch.hub.load('local', r'C:\Users\moco_\OneDrive\Documents\Python\GP2\GP2_files\yolov5x.pt')  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.