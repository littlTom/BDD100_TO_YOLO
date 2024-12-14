import json
from tqdm import tqdm
import cv2
import os

def dataset_invert(image_path, label_path, label_save_path, label_type):
    with open(label_path,'r') as fr:
       data = json.load(fr)
       for i in tqdm(range(len(data)), desc = 'Inverting BDD100 json to YOLO txt'):
           obj = data[i]
           try:
               empty = obj['labels']
           except KeyError:
               name = obj['name']
               txt = os.path.splitext(name)[0] + ".txt"
               with open(label_save_path + '/' + txt, 'a+') as fw:
                   fw.write('')
           else:
               name = obj['name']
               img = cv2.imread(image_path + '/' + name)
               # some invalid label may not have corresponding image files
               if img is not None:
                   txt = os.path.splitext(name)[0] + ".txt"
                   width, height = img.shape[1], img.shape[0]
                   dw = 1.0 / width
                   dh = 1.0 / height
                   for label in obj['labels']:
                       n = -1
                       for c in label_type:
                           n += 1
                           if label['category'] == c:
                               break
                       if n == -1:
                           with open(label_save_path + '/' + txt, 'a+') as fw:
                               fw.write('')
                       else:
                           roi = label['box2d']
                           w = roi['x2'] - roi['x1']
                           h = roi['y2'] - roi['y1']
                           x_center = roi['x1'] + w / 2
                           y_center = roi['y1'] + h / 2
                           x_center, y_center, w, h = x_center * dw, y_center * dh, w * dw, h * dh
                           with open(label_save_path + '/' + txt, 'a+') as fw:
                               fw.write(
                                   str(n) + ' ' + repr(x_center) + ' ' + repr(y_center) + ' ' + repr(w) + ' ' + repr(
                                       h) + '\n')


def dataset_fix(image_path, label_save_path):
    image_name = os.listdir(image_path)
    label_name = os.listdir(label_save_path)
    num_image = len(image_name)
    n_image_d = 0

    # clear invalid image
    for j in tqdm(range(num_image), desc = 'Scanning invalid images'):
        i = image_name[j]
        n = 0
        for l in label_name:
            if os.path.splitext(i)[0] == os.path.splitext(l)[0]:
                n += 1
        if n == 0:
            os.remove(image_path + '/' + i)
            n_image_d += 1