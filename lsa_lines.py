import cv2

# load the image and into grayscale
#img = cv2.imread('C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\lines3.jpg')


cropping = False
x1, y1, x2, y2 = 0, 0, 0, 0
img = cv2.imread('C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\lines3.jpg')
original = img.copy()

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
    i = img.copy()
    if not cropping:
        cv2.imshow("image", img)
    elif cropping:
        cv2.rectangle(i, (x1, y1), (x1, y1), (255, 0, 0), 2)
        cv2.imshow("image", i)

    cv2.waitKey(0)
cv2.destroyAllWindows()


# convert image into grayscale
gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

# threshold the image to reveal white regions in the image
thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]

# find the edges in the image using canny detector(binary image)
edges = cv2.Canny(thresh, 100, 200)

# Detect points that form "border lines" of the line
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)


# read image
img1 = cv2.imread('C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\lines3.jpg')

# convert image into grayscale
gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

# threshold the image to reveal white regions in the image
thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]

# to avoid 3D array in "lines"
l = lines.reshape(len(lines), -1)

# sorts to get the adjacent border lines together in the image
s = l[np.argsort(l[:, 1])]

# define points
mean = []
median = []
for i in range(0, len(s)):
    if (i % 2 == 0):
        # accessing the pixel values by its row and columns
        points = img1[((s[i][1]) - 20):((s[i + 1][3]) + 20),
                 s[i][0]:s[i + 1][2]]  # points = img1[y1:y2, x1:x2] Eg:[168:190, 16:148]

        # Display the grayscale intensities of the lines
        print("Grayscale intensities of line", i, ":\n\n", points)
        print("______________________________________")

        # Display their respective median and mean
        n = (len(s)) / 2
        m1 = np.mean(points)
        m2 = np.median(points)
        mean.append(m1)
        median.append(m2)
print("Median of the", n, "lines:", median)
print("Mean of the", n, "lines:", mean)


