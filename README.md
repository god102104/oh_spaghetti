# oh_spaghetti

KT 인턴십 1조 돌봐주개의 깃허브입니다

Main 기능 파일
1. 펫 인식 및 추적 기능
oh_spaghetti/findDog.py
oh_spaghetti/orange/car.py #주행

2. 밥 그릇 인식 및 잔량확인 기능
oh_spaghetti/dog_bowl.py
oh_spaghetti/orange/bowl.py#주행

3. 앱주소 
https://github.com/msShim/pet_butler

## Install
### 1. Update the Raspberry Pi
First, the Raspberry Pi needs to be fully updated. Open a terminal and issue:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
Depending on how long it’s been since you’ve updated your Pi, the upgrade could take anywhere between a minute and an hour.

### 2. Install TensorFlow
*Update 10/13/19: Changed instructions to just use "pip3 install tensorflow" rather than getting it from lhelontra's repository. The old instructions have been moved to this guide's appendix.*

Next, we’ll install TensorFlow. The download is rather large (over 100MB), so it may take a while. Issue the following command:

```
pip3 install tensorflow
```

TensorFlow also needs the LibAtlas package. Install it by issuing the following command. (If this command doesn't work, issue "sudo apt-get update" and then try again).
```
sudo apt-get install libatlas-base-dev
```
While we’re at it, let’s install other dependencies that will be used by the TensorFlow Object Detection API. These are listed on the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) in TensorFlow’s Object Detection GitHub repository. Issue:
```
sudo pip3 install pillow lxml jupyter matplotlib cython
sudo apt-get install python-tk
```
Alright, that’s everything we need for TensorFlow! Next up: OpenCV.

### 3. Install OpenCV
TensorFlow’s object detection examples typically use matplotlib to display images, but I prefer to use OpenCV because it’s easier to work with and less error prone. The object detection scripts in this guide’s GitHub repository use OpenCV. So, we need to install OpenCV.

To get OpenCV working on the Raspberry Pi, there’s quite a few dependencies that need to be installed through apt-get. If any of the following commands don’t work, issue “sudo apt-get update” and then try again. Issue:
```
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install qt4-dev-tools libatlas-base-dev
```
Now that we’ve got all those installed, we can install OpenCV. Issue:
```
sudo pip3 install opencv-python
```
Alright, now OpenCV is installed!

### 4. Compile and Install Protobuf
The TensorFlow object detection API uses Protobuf, a package that implements Google’s Protocol Buffer data format. You used to need to compile this from source, but now it's an easy install! I moved the old instructions for compiling and installing it from source to the appendix of this guide.

```sudo apt-get install protobuf-compiler```

Run `protoc --version` once that's done to verify it is installed. You should get a response of `libprotoc 3.6.1` or similar.

### 5. Set up TensorFlow Directory Structure and PYTHONPATH Variable
we need to modify the PYTHONPATH environment variable to point at some directories inside the TensorFlow repository we just downloaded. We want PYTHONPATH to be set every time we open a terminal, so we have to modify the .bashrc file. Open it by issuing:
```
sudo nano ~/.bashrc
```
Move to the end of the file, and on the last line, add:
```
export PYTHONPATH=$PYTHONPATH:/home/pi/oh_spaghetti/research:/home/pi/oh_spaghetti/research/slim
```

Then, save and exit the file. This makes it so the “export PYTHONPATH” command is called every time you open a new terminal, so the PYTHONPATH variable will always be set appropriately. Close and then re-open the terminal.

Now, we need to use Protoc to compile the Protocol Buffer (.proto) files used by the Object Detection API. The .proto files are located in /research/object_detection/protos, but we need to execute the command from the /research directory. Issue:
```
cd /home/pi/oh_spaghetti/research
protoc object_detection/protos/*.proto --python_out=.
```
This command converts all the "name".proto files to "name_pb2".py files. Next, move into the object_detection directory:

### 6. start

Run the script by issuing: 
```
python3 OD_with_socket.py 
```

## Appendix

### Old instructions for installing TensorFlow
These instructions show how to install TensorFlow using lhelontra's repository. They were replaced in my 10/13/19 update of this guide. I am keeping them here, because these are the instructions used in my [video](https://www.youtube.com/watch?v=npZ-8Nj1YwY).

In the /home/pi directory, create a folder called ‘tf’, which will be used to hold all the installation files for TensorFlow and Protobuf, and cd into it:
```
mkdir tf
cd tf
```
A pre-built, Rapsberry Pi-compatible wheel file for installing the latest version of TensorFlow is available in the [“TensorFlow for ARM” GitHub repository](https://github.com/lhelontra/tensorflow-on-arm/releases). GitHub user lhelontra updates the repository with pre-compiled installation packages each time a new TensorFlow is released. Thanks lhelontra!  Download the wheel file by issuing:
```
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v1.8.0/tensorflow-1.8.0-cp35-none-linux_armv7l.whl
```
At the time this tutorial was written, the most recent version of TensorFlow was version 1.8.0. If a more recent version is available on the repository, you can download it rather than version 1.8.0.

Alternatively, if the owner of the GitHub repository stops releasing new builds, or if you want some experience compiling Python packages from source code, you can check out my video guide: [How to Install TensorFlow from Source on the Raspberry Pi](https://youtu.be/WqCnW_2XDw8), which shows you how to build and install TensorFlow from source on the Raspberry Pi.

[![Link to TensorFlow installation video!](https://raw.githubusercontent.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi/master/doc/Install_TF_RPi.jpg)](https://www.youtube.com/watch?v=WqCnW_2XDw8)

Now that we’ve got the file, install TensorFlow by issuing:
```
sudo pip3 install /home/pi/tf/tensorflow-1.8.0-cp35-none-linux_armv7l.whl
```
TensorFlow also needs the LibAtlas package. Install it by issuing (if this command doesn't work, issue "sudo apt-get update" and then try again):
```
sudo apt-get install libatlas-base-dev
```
While we’re at it, let’s install other dependencies that will be used by the TensorFlow Object Detection API. These are listed on the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) in TensorFlow’s Object Detection GitHub repository. Issue:
```
sudo pip3 install pillow lxml jupyter matplotlib cython
sudo apt-get install python-tk
```
TensorFlow is now installed and ready to go!

### Old instructions for compiling and installing Protobuf from source
These are the old instructions from Step 4 showing how to compile and install Protobuf from source. These were replaced in the 10/13/19 update of this guide.

The TensorFlow object detection API uses Protobuf, a package that implements Google’s Protocol Buffer data format. Unfortunately, there’s currently no easy way to install Protobuf on the Raspberry Pi. We have to compile it from source ourselves and then install it. Fortunately, a [guide](http://osdevlab.blogspot.com/2016/03/how-to-install-google-protocol-buffers.html) has already been written on how to compile and install Protobuf on the Pi. Thanks OSDevLab for writing the guide!

First, get the packages needed to compile Protobuf from source. Issue:
```
sudo apt-get install autoconf automake libtool curl
```
Then download the protobuf release from its GitHub repository by issuing:
```
wget https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-all-3.5.1.tar.gz
```
If a more recent version of protobuf is available, download that instead. Unpack the file and cd into the folder:
```
tar -zxvf protobuf-all-3.5.1.tar.gz
cd protobuf-3.5.1
```
Configure the build by issuing the following command (it takes about 2 minutes):
```
./configure
```
Build the package by issuing:
```
make
```
The build process took 61 minutes on my Raspberry Pi. When it’s finished, issue:
```
make check 
```
This process takes even longer, clocking in at 107 minutes on my Pi. According to other guides I’ve seen, this command may exit out with errors, but Protobuf will still work. If you see errors, you can ignore them for now. Now that it’s built, install it by issuing:
```
sudo make install
```
Then move into the python directory and export the library path:
```
cd python
export LD_LIBRARY_PATH=../src/.libs
```
Next, issue:
```
python3 setup.py build --cpp_implementation 
python3 setup.py test --cpp_implementation
sudo python3 setup.py install --cpp_implementation
```
Then issue the following path commands:
```
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION_VERSION=3
```
Finally, issue:
```
sudo ldconfig
```
That’s it! Now Protobuf is installed on the Pi. Verify it’s installed correctly by issuing the command below and making sure it puts out the default help text.
```
protoc
```
For some reason, the Raspberry Pi needs to be restarted after this process, or TensorFlow will not work. Go ahead and reboot the Pi by issuing:
```
sudo reboot now
```

Protobuf should now be installed!

### Version
