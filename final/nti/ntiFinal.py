from time import time
from clover import srv
from clover.srv import GetTelemetry
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Float64MultiArray
import rospy
from std_srvs.srv import Trigger
import math
from pyzbar import pyzbar
from pyzbar.pyzbar import decode as qr_read
import cv2 as cv

rospy.init_node('flight')

navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)

bridge = CvBridge()
out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, (320, 240))
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)

qr_flag = 0


def image_callback(data):
    global out
    telemetry = get_telemetry(frame_id='aruco_map')
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')
    cv2.putText(cv_image, "x: " + str(round(telemetry.x, 2)), (0, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    cv2.putText(cv_image, "y: " + str(round(telemetry.y, 2)), (0, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    out.write(cv_image)
    cv2.imshow('Okno', cv_image)
    cv2.waitKey(1)


def qr_image_callback(data):
    global qr_flag
    frame = bridge.imgmsg_to_cv2(data, 'bgr8')
    barcodes = qr_read(frame)  # read the barcode using zbar
    if barcodes and qr_flag == 0:
        print(barcodes[0].data)
        # draw rect and publish to topic
        (x, y, w, h) = barcodes[0].rect
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        qr_flag = 1


image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

navigate(x=0, y=0, z=2, speed=1, frame_id='body', auto_arm=True)
rospy.sleep(3)
qr_image_sub = rospy.Subscriber('main_camera/image_raw', Image, qr_image_callback, queue_size=1)
rospy.sleep(0.05)
qr_image_sub.unregister()

navigate(x=8, y=0.95, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)
navigate(x=8.98, y=8.88, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=3.64, y=6.25, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)
sens_sub = rospy.wait_for_message('sensors', Float64MultiArray).data
print('Temperature:', sens_sub[0])
print('Gaz:', sens_sub[1:])

navigate(x=1.06, y=0.97, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=1.02, y=8.07, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)
sens_sub = rospy.wait_for_message('sensors', Float64MultiArray).data
print('Temperature:', sens_sub[0])
print('Gaz:', sens_sub[1:])

navigate(x=8.27, y=4.73, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=3.29, y=3.06, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)
sens_sub = rospy.wait_for_message('sensors', Float64MultiArray).data
print('Temperature:', sens_sub[0])
print('Gaz:', sens_sub[1:])

navigate(x=5.40, y=0.03, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)
sens_sub = rospy.wait_for_message('sensors', Float64MultiArray).data
print('Temperature:', sens_sub[0])
print('Gaz:', sens_sub[1:])

navigate(x=0.84, y=4.93, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=6.24, y=7.04, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=0, y=0, z=2, speed=4, frame_id='aruco_map')
rospy.sleep(7)

land()
rospy.sleep(3)
