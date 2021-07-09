

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

#이미지 256x256 pixel로 전처리
catg = ["Full", "Empty"]

def Dataization(img): #cv2 image box size setting 
    image_w = 256
    image_h = 256
    #img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=image_w/img.shape[1], fy=image_h/img.shape[0])

    return (img/256)


# 카메라 사진 사이즈 설정
IM_WIDTH = 320    #Use smaller resolution for
IM_HEIGHT = 240   #slightly faster framerate


sys.path.append('..')

# Import utilites
sys.path.append('research/')
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# 사용할 object detection model directory 설정
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

CWD_PATH = os.getcwd()

# frozen detection graph .pb file의 path 설정(사용할 모델)
PATH_TO_CKPT = os.path.join(CWD_PATH,'research','object_detection',MODEL_NAME,'frozen_inference_graph.pb')

# label 파일 path 설정
PATH_TO_LABELS = os.path.join(CWD_PATH, 'research','object_detection','data','mscoco_label_map.pbtxt')

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

global frame

# 카메라 송출 및 물체를 detect하는 함수.
def OD():
    global frame
    global camera

    # Initialize frame rate calculation
    frame_rate_calc = 1

    #opencv를 통한 카메라 송출 
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

    # 오렌지 파이와 통신을 위한 소켓 설정
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(usr.ADDR2)
    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()
        
        # 카메라 프레임을 [1, None, None, 3] 차원으로 바꾸기 위한 계산
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)

        # input image frame을 model로 물체를 판별
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # 결과 출력 및 bounding box 그려주기
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

        # 이미지 출력
        cv2.imshow('Object detector', frame)

        # 찾은 물체의 이름을 판별. (bowl이 정답이지만 유사한것도 찾기 때문에 예외처리를 해줌.)
        if data_ and (data_[0] == 'bowl' or data_[0] =='potted plant' or data_[0] == 'boat' or data_[0] == 'sink' or data_[0] == 'frisbee'):
          # 물체의 이름, 물체 좌표의 중앙값을 오렌지 파이로 전송
          clientSocket.send((data_[0]+";"+str(data_[1])).encode())
        else:
          clientSocket.send("noData".encode())
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        data = clientSocket.recv(1024)
        data = data.decode()

        # 오랜지파이로부터 그릇을 찾았다는 데이터를 받으면 실행
        if data == "Find":
          clientSocket.close()
          return data_[0]
        if cv2.waitKey(1) == ord('q'):
            break
        rawCapture.truncate(0)

    camera.close()


    cv2.destroyAllWindows()
    sess.close()

# 밥 그릇에 먹이가 어느 정도인지 확인하는 기능
def check(data):
  global frame
  if data == 'bowl' or data =='boat' or data == 'potted plant' or data == 'sink' or data == 'frisbee':
    src = []
    name = []
    test = []
    test.append(Dataization(frame))
    test = np.array(test)

    # 학습 시킨 모델을 통해 먹이의 양을 판단
    model = load_model('bowl_kt2.h5')
    predict = model.predict_classes(test)
    for i in range(len(test)):
        return str(catg[predict[i]])

def remain_food_check():
    time.sleep(5)
    return check(OD())

if __name__ == "__main__":
    print(remain_food_check())
