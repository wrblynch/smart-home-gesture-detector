# Final Project - Home Assistant Facial Detection
## Ihyun Park A16605545
## William Lynch A14588777

---

### Design Project:

For our design project, we created a prototype of a home-alarm system that uses facial recognition and hand gestures to send MQTT commands to a home assistant server.  The overall flow for the project is that a button on the ESP32 is pressed to turn on the camera and facial recognition.  If the camera detects an approved face it will wait for a certain hand gesture.  In our example it waits for a thumbs up, which prompts the system to send the command to the server where action is taken on the command. 

![Image Caption](images/diagram.jpg)

This project was inspired by Will's family.  His Uncles, Grandpa and parents all use the home assistant software to run their smart home and security functions.  Our project looks to make the issuing of commands a hands free experience, currently a phone app or keypad is used to issue commands.  Being able to just use hand gestures would streamline the command process. Ideally this could be used by any one using the open source home assistant OS. 

We used the YOLO (You Only Look Once) algorithm to train our model for face and gesture detection. We chose this method as YOLO is the most consistent and accurate open source object detection method. Using the provided method, we trained our own model to detect a specific face and gestures. For demonstration purposes, we chose to train the model specifically for Ihyun's face and a thumbs up gesture, so that we can show how it treats undetected face and gestures. In the future, if we were to develop this project further than a simple prototype, we could implement a system that allows a user to take photos of their own face and gestures and have it trained within the system or our server in order to automatically add it to a list of detected faces and gestures for commercial use. The training process would be fulfilled by having the system take multiple pictures per second, then use image pre-processing in order to turn the image into a binary image via thresholding, then draw the bounding boxes around the largest contour, which in this case would be either the face or the gesture. Then have the user input the label for each set, for example, if we were to train this system for Will's face, we would have the camera take a video of will for a few seconds, saving each frame as an image. Then draw the bounding boxes around Will's face in all of the pictures, and Will will tell the system that those images are of Will. Then those images with the according bounding box coordinates and labels will be put through our YOLO train.py code, which will train and update the existing model, allowing to add Will as an authorized user.

We chose to implement a button through our MCU to activate the home alarm system, so that the face detection method is not active 24/7 and the user can activate it only when they need to access it. A use case for this would be if we create a smart home system that connects the home security to one server. Here, if the user presses the button in the front door, it will activate the face detection system, and when an authorized face is detected, they can gesture to either open or lock the door etc. which will send a message to the server using the MQTT protocol and perform the according command. This is where the MQTT protocol would come in handy, as it will allow for the server to be up consistently due to its lightweightness and save power thanks to its subscribe/publish model. This problem is worth addressing, as many

Specifically for our prototype, when the button is pressed on the MCU, it sends a message to our Python code that tells it to start its face detection, and when it detects an authorized face, it begins to scan for hand gestures, and when it detects a proper hand gesture, it sends a message to our server.

For presentation purposes and for easy testing by TAs our submitted implementation uses UDP to communicate the commands to a server.  In an MQTT setup a broker and homeassistant VM are necessary and this is a time consuming environment to set up, so for our purposes we will be using UDP as a proof of concept.  

As far as future improvements to our project, streamlining the process of adding new faces and gestures to the database would be useful.  Implementing these features so that people without computing experience could use it seamlessly.  

[![Project Demo](https://youtu.be/sDTXQB-r7To/0.jpg)](https://youtu.be/sDTXQB-r7To "Project Demo")

---