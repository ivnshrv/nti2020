import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Float64MultiArray

rospy.init_node("video_ros") # Name 
bridge = CvBridge()


temerature = 0
 

def callback(message):
    global temerature
    temerature = message.data[0]


def image_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data , 'bgr8')
    cv2.putText(cv_image, str(temerature), (0, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0)) #RGB HEX HSV BGR
    cv2.imshow("ivan", cv_image)
    cv2.waitKey(1)


image_sub = rospy.Subscriber("main_camera/image_raw", Image, image_callback)

rospy.Subscriber("/sensors", Float64MultiArray, callback)

while not rospy.is_shutdown():
    pass