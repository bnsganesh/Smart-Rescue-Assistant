"""                             Smart-Rescue Asst. developed by Team Evolvers, Acharya Nagarjuna University

                                Python Implementation for
                                    1. Recognition the People and counting persons in the Live Feed from Web-Cam or FPV
                                    2. Accesing the GPS Lat and Long when Detected
                                    3. Sending the Lat, Long and Person's Count to Mobile as SMS using GSM/GPRS SIM900A
                                    4. At the Same time, Sending the same data to CloudChip Api for Data Visualisation
                                For More details contact http://www.github.com/bnsganesh                                                    """
	


# Packages required for Object Recognition
import cv2
import numpy as np
import time

# Package required to trigger when Person Recognised
from alert_ground import *

# Loading Dataset
net = cv2.dnn.readNet("weights/weight-file.weights", "cfg/cfg-file.cfg")
classes = []
with open("label-file.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Accesing the Live Feed or FPV or Webcam 
cap = cv2.VideoCapture(0)

# Looping Variables
count=50
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

# Performing Frame by Frame
while True:
    _, frame = cap.read()
    frame_id += 1

    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Preparing Info for Showing on the Screen
    class_ids = []
    confidences = []
    boxes = []
    count=0
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Retreving Accuracy or Confidence
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
    k = 0

    # Identifying the Recognised-Object
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]]).lower()

            # Considering only Person from the Recognised Objects
            if label == 'person':
                if (count%50==0):
                    k = k + 1
                    confidence = confidences[i]
                    color = colors[class_ids[i]]

                    # Identifying person in the Frame and making Boundry
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 2)

                    # Triggering respective operation for Person Detection
                    trigger(pcount)


    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    
    # Person's Count
    pcount=k

    # Displaying prepared Info on the Screen
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
    
    # Displaying the Frame with Recognised Boundaries
    cv2.imshow("Image", frame)

    # Counting the Frames
    count = count+1     

    # To Exit
    key = cv2.waitKey(1)    
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


