



flag_qr = 0

# Image subscriber callback function
def qrimage_callback(data):
    cv_image = bridge.imgmsg_to_cv2(data, 'bgr8')  # OpenCV image
    barcodes = pyzbar.decode(cv_image)
    for barcode in barcodes:
        b_data = barcode.data.encode("utf-8")
        b_type = barcode.type
        (x, y, w, h) = barcode.rect
        xc = x + w/2
        yc = y + h/2
        #print("Found {} with data {} with center at x={}, y={}".format(b_type, b_data, xc, yc))
        if flag_qr == 0:
            print("{}".format(b_data))
            flag_qr = 1


qrimage_sub = rospy.Subscriber('main_camera/image_raw', Image, qrimage_callback, queue_size=1)
rospy.spin()