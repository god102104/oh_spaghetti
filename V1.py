# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import sys
from socket import *
from select import *
import user_setting as usr
# This is needed since the working directory is the object_detection folder.
sys.path.append('..')
sys.path.append('research/')
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

def ObjectDetection(cs):
    IM_WIDTH = 320    #Use smaller resolution for
    IM_HEIGHT = 240   #slightly faster framerate
# Name of the directory containing the object detection module we're using
    MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

# Grab path to current working directory
    CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,'research','object_detection',MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH,'research','object_detection','data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
    NUM_CLASSES = 90

## Load the label map.
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

    # Each box represents a part of the image where a particular object was detected
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represents level of confidence for each of the objects.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    # Number of objects detected
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    # Initialize frame rate calculation
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)
    flag = False
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
            line_thickness=8,
            min_score_thresh=0.40)
        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
        clientSocket = socket(AF_INET, SOCK_STREAM)# 소켓을 생성한다.
       # print(data_)
        clientSocket.connect(usr.ADDR)
#        print(str(distance))
        if data_ and ("dog" == data_[0] or "cat" == data_[0]):
          if flag == False:
              flag = True
              cs.send("Find".encode())
          clientSocket.send((data_[0]+";"+str(data_[1])).encode())
          #print('connect is success')
        else:
          clientSocket.send("noData".encode())
      #    print("nodata")
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            print("end")
            clientSocket = socket(AF_INET, SOCK_STREAM)#
            clientSocket.connect(usr.ADDR)
            clientSocket.send("end".encode())
            break
        if cv2.waitKey(3) == ord('r'):
            print("check")
            clientSocket.send("re".encode())
        rawCapture.truncate(0)

    camera.close()

 # cv2.destroyAllWindows()

if __name__ == "__main__":
    ObjectDetection()
    cv2.detroyAllWindows()
