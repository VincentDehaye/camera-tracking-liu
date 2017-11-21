import _init_paths
import tensorflow as tf
from networks.factory import get_network
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import PoseStamped
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
import matplotlib.pyplot as plt

import cv2
import numpy as np
import rospy
import message_filters

import time
import math

MODEL_FILE = "datasets/models/VGGnet_fast_rcnn_iter_70000.ckpt"
CAMERA_TOPCI = "/lq0/camera0/image_color/compressed"
POSE_TOPIC = "/lq0/pose"

class RosbagImporter:
	def __init__(self,image_topic,pose_topic):
		rospy.init_node('detector')
		# rospy.Subscriber(image_topic, CompressedImage, image_callback)
		# rospy.Subscriber(pose_topic, PoseStamped, pose_callback)
		# rospy.spin()
		image_sub 	= message_filters.Subscriber(image_topic,CompressedImage)
		pose_sub 	= message_filters.Subscriber(pose_topic, PoseStamped)
		ts = message_filters.ApproximateTimeSynchronizer([image_sub,pose_sub], 40, 0.1)
		ts.registerCallback(image_callback)
		rospy.spin()


def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]
        cv2.rectangle(im,(bbox[0],bbox[1]),(bbox[2], bbox[3]), (255,0,0),2)
        # Height of box in pixels
        height = str(bbox[3] - bbox[1])
        print "Height of box",i,":",height,"px"
        cv2.putText(im, height,(bbox[0], bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('output',im)
    cv2.waitKey(1); 

def image_callback(image,pose):
	pos = pose.pose.position
	print(math.sqrt(pos.x*pos.x + pos.y*pos.y + pos.z*pos.z))


	np_arr = np.fromstring(image.data, np.uint8)
	cv2_img = cv2.imdecode(np_arr, 1)

	start = time.time()
	scores, boxes = im_detect(session, network, cv2_img)
	CONF_THRESH = 0.8
	NMS_THRESH = 0.3
	cls_ind = 15
	cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
	cls_scores = scores[:, cls_ind]
	dets = np.hstack((cls_boxes,cls_scores[:, np.newaxis])).astype(np.float32)
	keep = nms(dets, NMS_THRESH)
	dets = dets[keep, :]
	end = time.time()
	print "Time for detector: ",end - start
	vis_detections(cv2_img, 'person', dets, thresh=CONF_THRESH)

# init session
session = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
# load network
network = get_network("_test_")
# load model
saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
saver.restore(session,MODEL_FILE)

#sess.run(tf.initialize_all_variables())
print '\n\nLoaded network {:s}'.format(MODEL_FILE)

importer = RosbagImporter(CAMERA_TOPCI,POSE_TOPIC)