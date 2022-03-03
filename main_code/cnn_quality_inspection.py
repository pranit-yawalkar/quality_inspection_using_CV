import cv2
from numpy import empty
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
from keras.preprocessing.image import img_to_array

path = os.path.join(os.getcwd(), "model_new.h5")
model = load_model(path)
labels = ["defective", "ok"]
cascade_path = "C:\\My Data\\Project\\code\\realtime\\haarcascades\\haarcascade_gear.xml"
cameraNo = 0
objectName = "Gear"
frameWidth = 512
frameHeight = 512
ok_color = (0, 255, 0)
defect_color = (0, 0, 255)

cp = cv2.VideoCapture(cameraNo, cv2.CAP_DSHOW)
cp.set(3, frameWidth)
cp.set(4, frameHeight)

cv2.namedWindow("Quality Inspection")
cv2.resizeWindow("Quality Inspection", frameWidth, frameHeight+100)
cv2.createTrackbar("Scale", "Quality Inspection", 400, 1000, empty)
cv2.createTrackbar("Min Area", "Quality Inspection", 50000, 100000, empty)
cv2.createTrackbar("Brightness", "Quality Inspection", 180, 255, empty)

cascade = cv2.CascadeClassifier(cascade_path)

while True:
    # Set camera brightness using trackbar
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Quality Inspection")
    cp.set(10, cameraBrightness)

    # Get camera image and convert to grayscale
    success, img = cp.read()
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # gray = cv2.resize(gray, (512, 512))
    # Detect the object using cascade
    scaleVal = 1+(cv2.getTrackbarPos("Scale", "Quality Inspection")/1000)
    objects = cascade.detectMultiScale(img, scaleVal)
    # Display the detected objects
    for(x,y,w,h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min Area", "Quality Inspection")
        if(area>minArea):
            
            roi_gray = img[y:y+h, x:x+w]
            print(roi_gray)
            roi_gray = cv2.resize(roi_gray, (256, 256))
            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype("float")/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)
                # roi = np.expand_dims(roi, axis=0)
                # print(roi_color[0])
                prediction = model.predict(roi)
                print(prediction)
                # break
                label = labels[prediction.argmax()]
                label_position = (x+70, y-5)
                if(label=="defective"):
                    cv2.rectangle(img, (x,y), (x+w, y+h), defect_color, 3)
                    cv2.putText(img, objectName, (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, defect_color, 2)
                    cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, defect_color, 2)
                else:
                    cv2.rectangle(img, (x,y), (x+w, y+h), ok_color, 3)
                    cv2.putText(img, objectName, (x, y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, ok_color, 2)
                    cv2.putText(img, label, label_position, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, ok_color, 2)
            else:
                cv2.putText(img, "No gear", (30, 80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, ok_color, 2)
    
    cv2.imshow("Quality Inspection", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cp.release()
cv2.destroyAllWindows()