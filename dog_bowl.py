

# Import packages
import os, re, glob
import cv2
import numpy as np
import shutil
from numpy import argmax
from keras.models import load_model
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import sys
import time
import user_setting as usr
from socket import *
import asyncio
from picam import *

#############################################
#-----------insert bolw detection------------

catg = ["Full", "Empty"]

def Dataization(img): #cv2 image box size setting 
    image_w = 256
    image_h = 256
    #img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=image_w/img.shape[1], fy=image_h/img.shape[0])

    return (img/256)


#############################################


# Set up camera constants
IM_WIDTH = 320    #Use smaller resolution for
IM_HEIGHT = 240   #slightly faster framerate


# This is needed since the working directory is the object_detection folder.
sys.path.append('..')

# Import utilites
sys.path.append('research/')
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,'research','object_detection',MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, 'research','object_detection','data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 90

## Load the label map.
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine

#
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

if not picam_check:
    picam_check = True

global frame

def OD():
    global frame
    global camera
    # Initialize frame rate calculation
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    font = cv2.FONT_HERSHEY_SIMPLEX
    try:
        camera._check_camera_open()
    except Exception as e:
        if e.__class__.__name__ =="PiCameraClosed":
         camera = PiCamera()
         camera.resolution = (320,240)
         camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))     
    rawCapture.truncate(0)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(usr.ADDR2)
    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()
        
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
        data_ = vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            skip_labels=True,
            use_normalized_coordinates=True,
            max_boxes_to_draw = 1,
            line_thickness=8,
            min_score_thresh=0.40)
        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
        if data_ and (data_[0] == 'bowl' or data_[0] =='potted plant' or data_[0] == 'boat' or data_[0] == 'sink' or data_[0] == 'frisbee' or data_[0] == 'toilet'):
          clientSocket.send((data_[0]+";"+str(data_[1])).encode())
        else:
          clientSocket.send("noData".encode())
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        data = clientSocket.recv(1024)
        data = data.decode()
        if data == "Find":
          clientSocket.close()
          return data_[0]
        if cv2.waitKey(1) == ord('q'):
            break
        rawCapture.truncate(0)

    camera.close()


    cv2.destroyAllWindows()
    sess.close()

def check(data):
  global frame
  if data == 'bowl' or data =='boat' or data == 'potted plant' or data == 'sink' or data == 'frisbee' or data == 'toilet':
    src = []
    name = []
    test = []
    test.append(Dataization(frame))
    test = np.array(test)
    model = load_model('bowl_kt2.h5')
    predict = model.predict_classes(test)
    for i in range(len(test)):
        return str(catg[predict[i]])
        #print("Predict :" + str(catg[predict[i]]))

def remain_food_check():
    time.sleep(5)
    return check(OD())

if __name__ == "__main__":
    print(remain_food_check())
