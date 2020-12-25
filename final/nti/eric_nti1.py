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

rospy.init_node('flight')

navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

bridge = CvBridge() 
out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (320, 240))
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
telemetry = get_telemetry()

def image_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')
    cv2.putText(cv_image, str(telemetry.x), (0, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv2.putText(cv_image, str(telemetry.y), (0, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv2.putText(cv_image, str(telemetry.z), (0, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    out.write(cv_image)
    cv2.imshow('Okno', cv_image)
    cv2.waitKey(1)

image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback)

navigate(x=0, y=0, z=1.5, speed=1, frame_id='body', auto_arm=True)
rospy.sleep(3)

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