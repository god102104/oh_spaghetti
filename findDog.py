# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import time
import sys
from threading import Thread
from socket import *
from select import *
import user_setting as usr
# This is needed since the working directory is the object_detection folder.
sys.path.append('..')
sys.path.append('research/')
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from picam import *

# 사용할 object detection model directory 설정
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# frozen detection graph .pb file의 path 설정(사용할 모델)
PATH_TO_CKPT = os.path.join(CWD_PATH,'research','object_detection',MODEL_NAME,'frozen_inference_graph.pb')

# label 파일 path 설정
PATH_TO_LABELS = os.path.join(CWD_PATH,'research','object_detection','data','mscoco_label_map.pbtxt')

NUM_CLASSES = 90

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# 모델을 읽어와서 텐서플로우 그래프 생성
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Input tensor 값
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors는 boxes, scores, and classes를 찾아줍니다.
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# 각 dectect된 object의 점수값을 보여줍니다.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
# 각 dectect된 object의 종류를 보여줍니다.
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# 찾아진 물체의 갯수
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# 파이카메라 중복 실행을 막기위한 코드
if not picam_check:
    picam_check = True

global Sdata

# 안드로이드와 소켓통신하여 다음 명령이 입력되었을 때 findDog 명령 종료(thread 사용)
def check(cs):
    global Sdata
    while True:
        Sdata = cs.recv(1024)
        Sdata = Sdata.decode()
        if Sdata != "1\n":
           break

# 카메라 송출 및 물체를 detect하는 함수.
def ObjectDetection(t): 
    global camera
    time.sleep(5) 

    #opencv를 통한 카메라 송출
    frame_rate_calc = 1
    freq = cv2.getTickFrequency() #tick frequency -> for measuring actural clock cycle 
    font = cv2.FONT_HERSHEY_SIMPLEX 
    try:
        camera._check_camera_open()
    except Exception as e:
        if e.__class__.__name__== "PiCameraClosed": 
         camera = PiCamera()
         camera.resolution = (320, 240) #setting camera resolution
         camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))     
    rawCapture.truncate(0) #clear stream for next frame

    # 오렌지 파이와 통신을 위한 소켓 설정
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(usr.ADDR)
    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True): #output= rawCapture 
        t1 = cv2.getTickCount() #counting cycle
        if not t.is_alive():
            print("aLive")
            clientSocket.send("end".encode())
            break

        # 카메라 프레임을 [1, None, None, 3] 차원으로 바꾸기 위한 계산 
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0) 

        # input image frame을 model로 물체를 판별
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # 결과 출력 및 bounding box 그려주기.
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

        
        # 이미지 출력
        cv2.imshow('Object detector', frame)

        # 찾은 물체의 이름을 판별. (dog가 정답이지만 유사한것도 찾기 때문에 예외처리를 해줌.)
        if data_ and ("dog" == data_[0] or "cat" == data_[0]):
          # 물체의 이름, 물체 좌표의 중앙값을 오렌지 파이로 전송   
          clientSocket.send((data_[0]+";"+str(data_[1])+";").encode())
        else:
          clientSocket.send("noData".encode())
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        rawCapture.truncate(0)
        if cv2.waitKey(1) == 'q':
            break


    camera.close()

    cv2.destroyAllWindows()

def findDog(cs):
    #안드로이드와 통신과 물체인식을 동시에 진행하기 위해 thread 사용
    t1 = Thread(target = check, args = (cs,))
    t1.start()
    ObjectDetection(t1)
    t1.join()
    time.sleep(5)
 
    return Sdata

if __name__ == "__main__":
    ObjectDetection()
