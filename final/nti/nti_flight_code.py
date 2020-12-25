import rospy
from clover import srv
from std_srvs.srv import Trigger
import math

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

navigate(x=0, y=0, z=1.5, speed=1, frame_id='body', auto_arm=True)
rospy.sleep(3)

navigate(x=8, y=0.95, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=8.98, y=8.88, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=3.64, y=6.25, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=1.06, y=0.97, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=1.02, y=8.07, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=8.27, y=4.73, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=3.29, y=3.06, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=5.40, y=0.03, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=0.84, y=4.93, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=6.24, y=7.04, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)

navigate(x=0, y=0, z=2, speed=2, frame_id='aruco_map')
rospy.sleep(7)
land()
