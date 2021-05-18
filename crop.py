import cv2

cropping = False
x1, y1, x2, y2 = 0, 0, 0, 0
image = cv2.imread('D:\dog.jpg')
original = image.copy()

def mouse_crop(event, x, y, flags, param):
    global x1, y1, x2, y2, cropping
	# if the left mouse button was DOWN, start RECORDING and the (x, y) coordinates and indicate that cropping has began
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1, x2, y2 = x, y, x, y
        cropping = True
	# Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x2, y2 = x, y
	# if the left mouse button was released, record the ending (x, y) coordinates
    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
		# cropping is finished
        cropping = False
        refPoint = [(x1, y1), (x2, y2)]
		# when two points were found
        if len(refPoint) == 2:
            roi = original[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped Image", roi)
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)

while True:
    i = image.copy()
    if not cropping:
        cv2.imshow("image", image)
    elif cropping:
        cv2.rectangle(i, (x1, y1), (x1, y1), (255, 0, 0), 2)
        cv2.imshow("image", i)

    cv2.waitKey(0)
cv2.destroyAllWindows()