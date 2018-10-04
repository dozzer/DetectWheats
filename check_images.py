from xml.etree import ElementTree
from glob import glob as xmlFiles

from urllib.request import urlopen
import os

import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

# %matplotlib inline

ann_folder = "annotations/xmls"
img_folder = "images"

BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)


# -----------------

def visualize_bbox(img, bbox, color=BOX_COLOR, thickness=2):
    x_min, y_min, x_max, y_max = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_max), int(y_min), int(y_max)
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    return img


def visualize(annotations, id):
    img = annotations['image'].copy()
    for idx, bbox in enumerate(annotations['bboxes']):
        img = visualize_bbox(img, bbox)
    plt.figure(figsize=(3, 3))
    ax1 = fig.add_subplot(3, 3, id)
    ax1.imshow(img)

# ----------------

limit = 4
counter = 0

# fig = plt.figure()
f, axarr = plt.subplots(6, 2)

for tree in [ann_folder]:

    # category_id_to_name = {17: 'cat', 18: 'dog'}
    for file in xmlFiles(tree + '/*.xml'):
        xmlFile = ElementTree.parse(file)
        boxes = xmlFile.findall('object/bndbox')
        bboxes = []
        for box in boxes:
            xmin = box.find('xmin')
            ymin = box.find('ymin')
            xmax = box.find('xmax')
            ymax = box.find('ymax')
            box = [xmin.text, ymin.text, xmax.text, ymax.text]
            bboxes.append(box)
        img_file = img_folder + "/" + os.path.splitext(os.path.split(file)[1])[0] + ".jpg"
        # print(img_file)
        img = cv2.imread(img_file, cv2.COLOR_BGR2RGB)
        annotations = {'image': img, 'bboxes': bboxes, 'category_id': [18, 17]}
        visualize(annotations, counter + 1)
        counter = counter + 1
        if counter > limit:
            break
