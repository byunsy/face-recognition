import os
import sys
import glob
import cv2


def save_face(frame, p1, p2, filename):
    # Get center point coordinates
    cp = ((p1[0] + p2[0])//2, (p1[1] + p2[1])//2) 

    # Find the y-midpoint 
    y_midp = int(((p2[1] - p1[1]) // 2) * 1.25)

    # Cropping a square around the face
    # - from the cp xy points, subtract y-midpoint to get top left pt
    # -                        add y-midpoint to get bottom right pt
    crop = frame[ cp[1]-y_midp:cp[1]+y_midp, cp[0]-y_midp:cp[0]+y_midp ]

    # crop = frame[y1:y1+h, x1:x1+w]
    crop = cv2.resize(crop, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(filename, crop)


# Video Capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Camera open failed!')
    sys.exit()

# Network

model = './opencv_face_detector/res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = './opencv_face_detector/deploy.prototxt'

net = cv2.dnn.readNet(model, config)

if net.empty():
    print('Net open failed!')
    sys.exit()

# Output Directory & File Index

outdir = 'output'
prefix = outdir + '/face_'
file_idx = 1

try:
    if not os.path.exists(outdir):
        os.makedirs(outdir)
except OSError:
    print('output folter create failed!')

png_list = glob.glob(prefix + '*.png')
if len(png_list) > 0:
    png_list.sort()
    last_file = png_list[-1]
    file_idx = int(last_file[-8:-4]) + 1

# Read Frames

cnt = 0
while True:
    _, frame = cap.read()
    if frame is None:
        break

	# Face Detection

    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    detect = net.forward()

    detect = detect[0, 0, :, :]
    (h, w) = frame.shape[:2]

    for i in range(detect.shape[0]):
        confidence = detect[i, 2]
        if confidence < 0.8:
            break

		# Face found!

        x1 = int(detect[i, 3] * w)
        y1 = int(detect[i, 4] * h)
        x2 = int(detect[i, 5] * w)
        y2 = int(detect[i, 6] * h)

        # Save face image as a png file

        cnt += 1

        if cnt % 5 == 0:
            filename = '{0}{1:04d}.png'.format(prefix, file_idx)
            save_face(frame, (x1, y1), (x2, y2), filename)
            file_idx += 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0))

        label = 'Face: %4.3f' % confidence
        cv2.putText(frame, label, (x1, y1 - 1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
