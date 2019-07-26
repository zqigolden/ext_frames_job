import cv2
import os
import sys
import numpy as np
import shutil

def check_dark(img):
    if isinstance(img, str):
        img = cv2.imread(img)
    result = np.max(img, axis=2) - np.min(img, axis=2)
    return np.mean(result)

def run(aim):
    if os.path.isdir(aim):
        for i in os.listdir(aim):
            run(aim + '/' + i)
    elif 'jpg' in aim:
        score = check_dark(aim)
        if score < 6:
            #print('Is dark: %s'%aim)
            if not os.path.exists('dark'):
                os.makedirs('dark')
            shutil.move(aim, 'dark')
if __name__ == '__main__':
    run(sys.argv[1])
