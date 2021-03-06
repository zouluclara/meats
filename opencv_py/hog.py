#!/usr/bin/env python

from __future__ import print_function

# Based off of Adrian:
# https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/

import argparse
import sys
import time

import cv2

parser = argparse.ArgumentParser()
parser.add_argument('webcam', nargs='?', default='0')
parser.add_argument('--downsample', '-d', type=int, default=1)
args = parser.parse_args()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

try:
    webcam = int(args.webcam)
except ValueError:
    # not a webcam...
    webcam = args.webcam

cap = cv2.VideoCapture(webcam)

start = 0

while True:
    ret, image = cap.read()

    if not ret:
        print('Error grabbing')
        break

    print('FPS: {:.1f}'.format(1 / (time.time() - start)))

    if args.downsample > 1:
        # copy to make contiguous, without importing numpy as np
        image = image[::args.downsample, ::args.downsample, :].copy()

    start = time.time()
    rects, weights = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
    print('{:.1f} ms {} objects'.format(1000 * (time.time() - start), len(rects)))

    for (x, y, w, h), score in zip(rects, weights):
        # Draw a rectangle around the faces
        print('at ({}, {}) size {}x{} score {}'.format(x, y, w, h, score))
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, '%.3f' % score, (x, y-2), cv2.FONT_HERSHEY_SIMPLEX,
            0.8,  # font scale
            (0, 255, 0),
            2  # thickness
        )

    # Display the resulting frame
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
