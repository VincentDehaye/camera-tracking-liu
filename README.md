Repo for camera based object tracking and distance estimation.

The code can be found on the server under `~/camera-tracking`. 

Make sure the computer has CUDA and ROS installed.

## Getting started

* Start roscore (preferably in a differnet bash session)
* Clone this repo
* Install python dependencies with  `requirements.txt` and `pip`
* Go to src folder

Make sure the parameters  `MODEL_FILE`, `CAMERA_TOPCI`, and `POSE_TOPIC` are linking to the ros topics and model files repsectivly. (The files can be found in the repo https://gitlab.ida.liu.se/TDDE19-2017-3/Datasets)

* `python calibration.py`
* `python main.py`
* Start rosbag (preferably in a differnet bash session)

The output images go to the `detections` folder and `tracking` folder. Everything else goes to stdout.

### Kown bugs
 There is a bug where bounding boxes from the detection stage are persistent on tracking images. 