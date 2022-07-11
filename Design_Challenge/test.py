import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION

Object_classes = ['thumbs']

Object_colors = list(np.random.rand(80,3)*255)
Object_detector = OBJ_DETECTION('weights/best.pt', Object_classes)

# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
#print(gstreamer_pipeline(flip_method=0))

cap = cv2.VideoCapture(0)

if cap.isOpened():
    window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
    # Window
    while cv2.getWindowProperty("CSI Camera", 0) >= 0:
        ret, frame = cap.read()
        if ret:
            # detection process
            objs = Object_detector.detect(frame)

            # plotting
            for obj in objs:
                # print(obj)
                label = obj['label']
                score = obj['score']
                [(xmin,ymin),(xmax,ymax)] = obj['bbox']
                color = Object_colors[Object_classes.index(label)]
                frame = cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2) 
                frame = cv2.putText(frame, f'{label} ({str(score)})', (xmin,ymin), cv2.FONT_HERSHEY_SIMPLEX , 0.75, color, 1, cv2.LINE_AA)
                #print(xmin, xmax, ymin, ymax)
                print(objs)

        cv2.imshow("CSI Camera", frame)
        keyCode = cv2.waitKey(30)
        if keyCode == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Unable to open camera")
