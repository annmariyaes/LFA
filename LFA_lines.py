import cv2
import numpy as np
from skimage.color import rgb2gray

#load the image and into grayscale
img = cv2.imread('C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\lines3.jpg')

#convert image into grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#threshold the image to reveal white regions in the image
thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]

#find the edges in the image using canny detector(binary image)
edges = cv2.Canny(thresh, 100, 200)

# Detect points that form "border lines" of the line
lines = cv2.HoughLinesP(edges, 1, np.pi/180,50, minLineLength=50, maxLineGap=100)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)



# read image
img1 = cv2.imread('C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\lines0.jpg')

# convert image into grayscale
def conversionMethod(conv):
    if conv == "Gray":
        return cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    elif conv == "Luminance":
        return rgb2gray(img1)
    elif conv == "Red":
        print("its red!")
    elif conv == "Green":
        print("its green!")
    elif conv == "Blue":
        print("its blue!")
    else:
        print("Invalid input!")
conv = input("Enter any Conversion method: ")
conversion = conversionMethod(conv)


# threshold the image to reveal white regions in the image
def thresholdingMethod(thresh):
    if thresh == "OTSU":
        return cv2.threshold(conversion, 100, 255, cv2.THRESH_OTSU)[1]
    elif thresh == "TOZERO":
        return cv2.threshold(conversion, 100, 255, cv2.THRESH_TOZERO)[1]
    elif thresh == "BINARY":
        return cv2.threshold(conversion, 100, 255, cv2.THRESH_BINARY)[1]
    else:
        print("Invalid input!")
thresh = input("Enter any Thresholding method: ")
threshold = thresholdingMethod(thresh)


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