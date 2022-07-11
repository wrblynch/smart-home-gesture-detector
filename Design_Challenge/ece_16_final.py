import cv2
import numpy as np
from elements.yolo import OBJ_DETECTION
from ECE16Lib.Communication import Communication
from time import time
from socket import create_connection, AF_INET, SOCK_STREAM
import socket
import pygame

targetHost = '127.0.0.1'
targetPort = 9879

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((targetHost, int(targetPort)))

if __name__ == "__main__":
    Object_colors = list(np.random.rand(80,3)*255)

    faces = ['Leo']
    gests = ['thumbs up']

    comms = Communication('/dev/COM4', 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")
    cap = cv2.VideoCapture(0)

    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            message = str(message).strip()
            if message == 'pressed':
                Object_classes = ['Leo']
                Object_detector = OBJ_DETECTION('weights/best.pt', Object_classes)
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
                    try:
                        if label in faces:
                            print('Authorized face detected, beginning scan for commands.')
                            break
                    except:
                        pass
                    cv2.imshow("CSI Camera", frame)
                    keyCode = cv2.waitKey(30)
                    if keyCode == ord('q'):
                        break
                cv2.destroyAllWindows()
                Object_classes = ['thumbs up']
                Object_detector = OBJ_DETECTION('weights/best.pt', Object_classes)
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
                    try:
                        if label in gests:
                            print(label + "detected, performing appropriate action.")
                            mqttResponse = 'Gesture Detected'
                            clientSocket.send(mqttResponse.encode())
                            break
                    except:
                        pass
                    cv2.imshow("CSI Camera", frame)
                    keyCode = cv2.waitKey(30)
                    if keyCode == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()