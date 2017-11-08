import _init_paths
import tensorflow as tf
from networks.factory import get_network
from sensor_msgs.msg import CompressedImage
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
import matplotlib.pyplot as plt

import cv2
import numpy as np
import rospy

CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

MODEL_FILE = "datasets/models/VGGnet_fast_rcnn_iter_70000.ckpt"
CAMERA_TOPCI = "/lq0/camera0/image_color/compressed"

class RosbagImporter:
	def __init__(self,topic):
		rospy.init_node('image_listener')
		rospy.Subscriber(topic, CompressedImage, image_callback)
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

    cv2.imshow('output',im)
    cv2.waitKey(1); 

def image_callback(msg):
	np_arr = np.fromstring(msg.data, np.uint8)
	cv2_img = cv2.imdecode(np_arr, 1)

	scores, boxes = im_detect(session, network, cv2_img)
	CONF_THRESH = 0.8
	NMS_THRESH = 0.3
	for cls_ind, cls in enumerate(CLASSES[1:]):
		cls_ind += 1 # because we skipped background
		cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
		cls_scores = scores[:, cls_ind]
		dets = np.hstack((cls_boxes,cls_scores[:, np.newaxis])).astype(np.float32)
		keep = nms(dets, NMS_THRESH)
		dets = dets[keep, :]
		vis_detections(cv2_img, cls, dets, thresh=CONF_THRESH)

# init session
session = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
# load network
network = get_network("_test_")
# load model
saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
saver.restore(session,MODEL_FILE)

#sess.run(tf.initialize_all_variables())
print '\n\nLoaded network {:s}'.format(MODEL_FILE)

importer = RosbagImporter(CAMERA_TOPCI)