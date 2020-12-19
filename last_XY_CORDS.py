import rospy
from clover import srv
from std_srvs.srv import Trigger
import math
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Float64MultiArray
from time import time


rospy.init_node("video_ros") # Name 

bridge = CvBridge()

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)



temerature = 0

out = cv2.VideoWriter("nti.avi", cv2.VideoWriter_fourcc("M","J","P","G"), 10, (320, 240) )

def callback(message):
    global temerature
    temerature = message.data

def image_callback(data):
    global out, telemetry
    telemetry = get_telemetry(frame_id='aruco_map')

    cv_image = bridge.imgmsg_to_cv2(data , 'bgr8')
    cv2.putText(cv_image, "x: "+str(round(telemetry.x, 2)), (0,215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
    cv2.putText(cv_image, "y: "+str(round(telemetry.y, 2)), (0,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
    cv2.imshow("ivan", cv_image)
    out.write(cv_image)
    cv2.waitKey(1)


def screen_callback(data):
    global screen_sub
    cv_image = bridge.imgmsg_to_cv2(data , 'bgr8')
    cv2.putText(cv_image, "x: "+str(round(telemetry.x, 2)), (0,215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
    cv2.putText(cv_image, "y: "+str(round(telemetry.y, 2)), (0,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0))
    cv2.imwrite("images/{}.jpg".format(time())  ,   cv_image) 
    cv2.waitKey(1)

image_sub = rospy.Subscriber("main_camera/image_raw", Image, image_callback)
rospy.Subscriber("/sensors", Float64MultiArray, callback)

navigate(x=0, y=0, z=1.5, speed=0.5, frame_id='body', auto_arm=True)
rospy.sleep(6)

navigate(x=8, y=1, z=2, speed = 1, frame_id='aruco_map')
rospy.sleep(12)

screen_sub = rospy.Subscriber("main_camera/image_raw", Image, screen_callback)
screen_sub.unregister()
print(temerature)

navigate(x=0, y=0, z=2, speed = 1, frame_id='aruco_map')
rospy.sleep(12)
screen_sub = rospy.Subscriber("main_camera/image_raw", Image, screen_callback)
screen_sub.unregister()


land()
