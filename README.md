# oh_spaghetti

KT 인턴십 1조 돌봐주개의 깃허브입니다
https://github.com/god102104/oh_spaghetti

Main 기능 파일
1. 펫 인식 및 추적 기능
oh_spaghetti/findDog.py
oh_spaghetti/orange/car.py  #주행

2. 밥 그릇 인식 및 잔량확인 기능
oh_spaghetti/dog_bowl.py
oh_spaghetti/orange/bowl.py #주행

3. 앱주소 
https://github.com/msShim/pet_butler

4. Keras & tensorflow Version
Keras 2.2.5
tensorflow 1.14.0


## Install
### 1. Update the Raspberry Pi
라즈베리 파이 업데이트
```
sudo apt-get update
sudo apt-get dist-upgrade
```

### 2. Install TensorFlow

```
pip3 install tensorflow==1.14.0
```
LibAtlas package 설치
```
sudo apt-get install libatlas-base-dev
```
필요한 모듈 설치
```
sudo pip3 install pillow lxml jupyter matplotlib cython
sudo apt-get install python-tk
```

### 3. Install OpenCV
```
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install qt4-dev-tools libatlas-base-dev
```
```
sudo pip3 install opencv-python
```

### 4. Compile and Install Protobuf

```sudo apt-get install protobuf-compiler```

### 5. 텐서플로 디렉토리 구조와 파이썬 Path 설정
```
sudo nano ~/.bashrc
```
가장 밑 줄에 아래 내용 추가
```
export PYTHONPATH=$PYTHONPATH:/home/pi/oh_spaghetti/research:/home/pi/oh_spaghetti/research/slim
```
저장

path 설정
```
cd ~/oh_spaghetti/research
protoc object_detection/protos/*.proto --python_out=.
```

### 6. start

On Raspberry Pi
```
cd ~/oh_spagetti
python3 client_socket.py


```

On Orange Pi
```
cd ~/oh_spagetti/orange
sudo python3 client_socket.py

# CCTV 기능 수행을 위한 mjpg_streamer 실행 명령어 ip http://{OrangePiAddress}:8081/?action=stream 주소로 실행
mjpg_streamer -i "input_uvc.so" -o "output_http.so -p 8081 -w /usr/local/share/mjpg-streamer/www/"

```