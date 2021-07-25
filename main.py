import cv2
import csv
import numpy as np
from PIL import Image

from skimage.color import rgb2gray
from skimage.filters import threshold_li, threshold_yen, threshold_otsu, threshold_isodata, threshold_triangle

from kivy.metrics import dp
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty, StringProperty


# KivyMD is a collection of Material Design compliant widgets for use with, Kivy cross-platform graphical framework
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable



Builder.load_file('popup.kv')
Builder.load_file('tabs.kv')


class FileChoosePopup(Popup):
    load = ObjectProperty()



class Tab(TabbedPanel):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)



    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()



    def load(self, selection):
        global img, lines, img1
        self.file_path = str(selection[0])
        self.the_popup.dismiss()

        # Check for non-empty list i.e, file selected
        if self.file_path:
            self.ids.get_file.text = self.file_path

            # load the image and into grayscale
            img = cv2.imread(self.file_path)



    # Image cropping
    def mouse_crop(self):
        global imgCrop, imgResize
        # Resize the actual size of image to fit the screen properly
        imgResize = cv2.resize(img, (2500, 1500))

        # Selection of Region Of Interest
        roi = cv2.selectROI(imgResize)

        # Crop image
        imgCrop = imgResize[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        cv2.imshow("Image", imgCrop)
        cv2.waitKey(0)



    # Detection of how many lines are in the image
    def detect_lines(self):
        global lines, nlines

        # Convert image into grayscale
        gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY)

        # Threshold the image to reveal white regions in the image
        thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]

        # Find the edges in the image using canny detector(binary image)
        edges = cv2.Canny(thresh, 100, 200)

        # Detect points that form "border lines" of the line
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(imgCrop, (x1, y1), (x2, y2), (255, 0, 0), 3)
        nlines = len(lines)/2

        # Display the lines-detected image
        cv2.imwrite('detected_image.jpg', imgCrop)
        self.ids.detected_image.source = 'detected_image.jpg'

        # Only integer values are allowed to be the number of lines
        n = int(nlines)
        # Display of number of lines in the lines-detected image
        self.ids.lines.text = f'{n}'



    # Dropdown for the color conversion methods (Gray, Luminance, Red, Green, Blue)
    def spinner_clicked(self, value):
        global conversion

        def conversionMethod(conv):
            if conv == "Gray":
                return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            elif conv == "Luminance":
                return rgb2gray(img)

            elif conv == "Red":
                pil_img = Image.fromarray(img).convert('RGB')
                # Split into 3 channels
                r, g, b = pil_img.split()
                # Increase Reds
                r = r.point(lambda i: i * 1.2)
                # Decrease Greens
                g = g.point(lambda i: i * 0.9)
                # Decrease Blues
                b = b.point(lambda i: i * 0.9)
                # Recombine back to RGB image
                result = Image.merge('RGB', (r, g, b))
                np_img = np.array(result)
                return np_img

            elif conv == "Green":
                pil_img = Image.fromarray(img).convert('RGB')
                # Split into 3 channels
                r, g, b = pil_img.split()
                # Decrease Reds
                r = r.point(lambda i: i * 0.9)
                # Increase Greens
                g = g.point(lambda i: i * 1.2)
                # Decrease Blues
                b = b.point(lambda i: i * 0.9)
                # Recombine back to RGB image
                result = Image.merge('RGB', (r, g, b))
                np_img = np.array(result)
                return np_img

            elif conv == "Blue":
                pil_img = Image.fromarray(img).convert('RGB')
                # Split into 3 channels
                r, g, b = pil_img.split()
                # Decrease Reds
                r = r.point(lambda i: i * 0.9)
                # Decrease Greens
                g = g.point(lambda i: i * 0.9)
                # Increase Blues
                b = b.point(lambda i: i * 1.2)
                # Recombine back to RGB image
                result = Image.merge('RGB', (r, g, b))
                np_img = np.array(result)
                return np_img

            else:
                print("Invalid input!")
        conv = value
        conversion = conversionMethod(conv)
        pass



    # Check-box for the thresholding methods (Li, Yen, Otsu, Isodata, Triangle)
    checks = []
    def checkbox_clicked(self, instance, value, threshold):

        if value == True:
            Tab.checks.append(threshold)
            thresh = ''
            for x in Tab.checks:
                thresh = f'{thresh} {x}'

                def thresholdingMethod(thresh):
                    if thresh == "Li":
                        thresh = threshold_li(conversion)
                        li = conversion > thresh
                        return li

                    elif thresh == "Yen":
                        thresh = threshold_yen(conversion)
                        yen = conversion > thresh
                        return yen

                    if thresh == "Otsu":
                        thresh = threshold_otsu(conversion)
                        otsu = conversion > thresh
                        return otsu

                    elif thresh == "Isodata":
                        thresh = threshold_isodata(conversion)
                        isodata = conversion > thresh
                        return isodata

                    elif thresh == "Triangle":
                        thresh = threshold_triangle(conversion)
                        triangle = conversion > thresh
                        return triangle

                    else:
                        print("Invalid input!")

                thresh = threshold
                threshold = thresholdingMethod(thresh)

            pass
        else:
            Tab.checks.remove(threshold)
            thresh = ''
            for x in Tab.checks:
                thresh = f'{thresh} {x}'
            pass


    # Offset to the increase the area of cropped image for better calculations
    def slide_it(self, *args):
        global l, s, n, mean, median

        self.slide_text.text = str(int(args[1]))
        offset = int(args[1])

        # To avoid 3D array in "lines"
        l = lines.reshape(len(lines), -1)

        # Sorts to get the adjacent border lines together in the image
        s = l[np.argsort(l[:, 1])]

        mean = []
        median = []
        for i in range(0, len(s)):
            if (i % 2 == 0):
                # Accessing the pixel values by its row and columns
                points = imgCrop[((s[i][1])-offset) : ((s[i+1][3])+offset), s[i][0] : s[i+1][2]]  # points = img1[y1:y2, x1:x2] Eg:[168:190, 16:148]

                # Their respective median and mean
                n = (len(s)) / 2
                m1 = np.mean(points)
                m2 = np.median(points)
                mean.append(m1)
                median.append(m2)
        print("Median of the", n, "lines:", median)
        print("Mean of the", n, "lines:", mean)



    # Datatable for median and mean of selected image
    def datatable(self, *args):
        self.table = MDDataTable(pos_hint = {'center_x': 0.5, 'center_y': 0.5},
                                 size_hint = (1, 0.95),
                                 use_pagination = True,
                                 check = True,
                                 rows_num = 10,
                                 column_data = [("File name", dp(70)),
                                                ("Lines", dp(20)),
                                                ("Mean", dp(40)),
                                                ("Median", dp(30))],
                                 row_data = [(self.file_path,
                                              f"{j + 1}",
                                              mean[j],
                                              median[j])
                                    for j in range(int(n))],
                                 )

        self.table.bind(on_row_press = self.on_row_press)
        self.table.bind(on_check_press = self.on_check_press)
        self.ids.body.add_widget(self.table)


    def on_row_press(self, instance_table, instance_row):
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        print(instance_table, current_row)



    def download(self, *args):
        # Stores values of first image
        with open("Data Table.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Median", "Mean"])
            csvwriter.writerows([p for p in zip(median, mean)])



class Assays(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"
        return Tab()


if __name__ == '__main__':
    Assays().run()
