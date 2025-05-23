import cv2
import cvlib as cv

from cvlib.object_detection import draw_bbox
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import keras

video = cv2.VideoCapture(0)
labels = []

while True:
    ret, frame = video.read()
    bbox, label, conf = cv.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)

    cv2.imshow("Object Detection", output_image)

    for item in label:
        if item not in labels:
            labels.append(item)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



i = 0
new_sentence = []
for label in labels:
    if i == 0:
        new_sentence.append(label)
    else:
        new_sentence.append(" " + label)
    i += 1

print(" ".join(new_sentence))



