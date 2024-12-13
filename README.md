# BDD100_TO_YOLO
## Introduction
Invert bdd100 dataset to yolo dataset and fix dataset
## Preparation
Use pip to install the ./dist/bdd100_to_yolo-1.0.0-py3-none-any.whl into your python .venv
## Example
<pre><code>
#import modules
from bdd100_to_yolo import bdd100_to_yolo

#BD100k original image file path, BD100k original label file path and the path saving inverted label files
images_train_path = "bd100/images/train"
images_val_path = "bdd100/images/val"
labels_train_path = "bdd100_labels/det_train.json"
labels_val_path = "bdd100_labels/det_val.json"
labels_train_save_path = "bdd100/labels/train"
labels_val_save_path = "bdd100/labels/val"

#It is feasible to delete some lables you do not want or shuffle the list below, "pederstrain" corresponds class number 0, "car" corresponds class number 1 and the next follws the same rules as above.
classes = [
    "pedestrian",  
    # "rider",
    "car",
    "truck",
    "bus",
    # "train",
    "motorcycle",
    "bicycle",
    "traffic light",
    "traffic sign"
]

#Invert DBB100json to YOLO txt
bdd100_to_yolo.dataset_invert(images_train_path, labels_train_path, labels_train_save_path, classes)
bdd100_to_yolo.dataset_invert(images_val_path, labels_val_path, labels_val_save_path, classes)

#Some image files do not have corresponding label files or some label files do not have corresponding image files, so it is necessary to clear the invalid data. Warning that you must run the dataset_invert() to invert all dbb100 json files to yolo txt file then running the dataset_fix(). BDD100K has 10 000 images so it may take 1 - 3 hours to fix the dataset.
bdd100_to_yolo.dataset_fix(images_train_path, labels_train_save_path)
bdd100_to_yolo.dataset_fix(images_val_path, labels_val_save_path)
</code></pre>
