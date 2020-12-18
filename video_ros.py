import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

rospy.init_node("video_ros") # Name 
bridge = CvBridge()


def image_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data , 'bgr8')
    cv2.imshow("ivan", cv_image)
    cv2.waitKey(1)


image_sub = rospy.Subscriber("main_camera/image_raw", Image, image_callback)

while not rospy.is_shutdown():
    pass









