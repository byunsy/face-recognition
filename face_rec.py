import sys
import numpy as np
import cv2
import shutil

face_name = ['Sang Yoon Byun', 'Unidentified']

def face_recognition(recognition_net, crop):
    # gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    blob = cv2.dnn.blobFromImage(crop, 1 / 255., (128, 128))
    recognition_net.setInput(blob)
    prob = recognition_net.forward()  # prob.shape=(1, 3)

    _, confidence, _, maxLoc = cv2.minMaxLoc(prob)
    face_idx = maxLoc[0]

    return face_idx, confidence

detection_net = cv2.dnn.readNet('./opencv_face_detector/opencv_face_detector_uint8.pb',
                                './opencv_face_detector/opencv_face_detector.pbtxt')

if detection_net.empty():
    print('Detection Net open failed!')
    sys.exit()

recognition_net = cv2.dnn.readNet('./frozen_model/frozen_graph.pb')

if detection_net.empty():
    print('Recognition Net open failed!')
    sys.exit()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    detection_net.setInput(blob)
    detect = detection_net.forward()

    detect = detect[0, 0, :, :]
    (h, w) = frame.shape[:2]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.5:
            break

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        # Crop
        p1 = (x1, y1)
        p2 = (x2, y2)
        cp = ((p1[0] + p2[0])//2, (p1[1] + p2[1])//2)
        y_midp = int(((p2[1] - p1[1]) // 2) * 1.25)

        crop = frame[ max(0, cp[1]-y_midp):cp[1]+y_midp, 
                      max(0, cp[0]-y_midp):cp[0]+y_midp ]

        # crop = frame[y1:y2, x1:x2]
        face_idx, confidence = face_recognition(recognition_net, crop)

        if face_idx:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255))
            label = '{0}'.format(face_name[face_idx])
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))
            label = '{0}'.format(face_name[face_idx])
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 255, 0), 2, cv2.LINE_AA)

        # label = '{0}: {1:0.3f}'.format(face_name[face_idx], confidence)
        # label = '{0}'.format(face_name[face_idx])
        # cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
        #             0.8, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()