import cv2
import csv
import os
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

    def __init__(self):
        super().__init__()
        self.img = None
        self.conversion_method = "Gray"
        self.converted_img = None
        self.thresh_method = None
        self.thresh_img = None
        self.offset = 20
        self.lines = None

        self.mean = []
        self.median = []

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])

        # Check for non-empty list i.e, file selected
        if self.file_path.endswith(".jpg"):
            # size of actual file path is large, so it doesn't fit the text file box
            self.ids.get_file.text = os.path.basename(self.file_path)
            print("file_path")

            # load the image and into grayscale
            self.img = cv2.imread(self.file_path)
            self.the_popup.dismiss()
            self.mouse_crop()

    # Image cropping
    def mouse_crop(self):
        # Resize the actual size of image to fit the screen properly
        self.img = cv2.resize(self.img, (2000, 1000))

        # Selection of Region Of Interest
        roi = cv2.selectROI(self.img, showCrosshair=False)

        # Crop image
        self.img = self.img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        cv2.imwrite('cropped_image.jpg', self.img)
        self.ids.detected_image.source = 'cropped_image.jpg'
        cv2.destroyAllWindows()

    # Detection of how many lines are in the image
    def detect_lines(self):

        # Convert image into grayscale
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Threshold the image to reveal white regions in the image
        thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]

        # Find the edges in the image using canny detector(binary image)
        edges = cv2.Canny(thresh, 100, 200)

        # Detect points that form "border lines" of the line
        self.lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)
        for line in self.lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(self.img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        nlines = len(self.lines) / 2

        # Display the lines-detected image
        cv2.imwrite('detected_image.jpg', self.img)
        self.ids.detected_image.source = 'detected_image.jpg'

        # Only integer values are allowed to be the number of lines
        n = int(nlines)
        # Display of number of lines in the lines-detected image
        self.ids.lines.text = f'{n}'

    # Dropdown for the color conversion methods (Gray, Luminance, Red, Green, Blue)
    def spinner_clicked(self, value):
        self.conversion_method = value

    def set_thresh_method(self, method):
        self.thresh_method = method

    def set_offset(self, offset):
        self.offset = int(offset)

    def apply_background_correction(self):
        img = self.img
        conv = self.conversion_method

        ## CONVERSION

        if conv == "Gray":
            self.converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        elif conv == "Luminance":
            self.converted_img = rgb2gray(img)

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
            self.converted_img = np_img

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
            self.converted_img = np_img

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
            self.converted_img = np_img
        else:
            print("Conversion: Invalid input!")

        ## THRESHOLDING
        thresh = self.thresh_method
        conversion = self.converted_img

        if thresh == "Li":
            thresh = threshold_li(conversion)
            self.thresh_img = conversion > thresh

        elif thresh == "Yen":
            thresh = threshold_yen(conversion)
            self.thresh_img = conversion > thresh

        elif thresh == "Otsu":
            thresh = threshold_otsu(conversion)
            self.thresh_img = conversion > thresh

        elif thresh == "Isodata":
            thresh = threshold_isodata(conversion)
            self.thresh_img = conversion > thresh

        elif thresh == "Triangle":
            thresh = threshold_triangle(conversion)
            self.thresh_img = conversion > thresh
        else:
            print("Threshold: Invalid input!")

        ## ANALYSE LINES
        offset = self.offset

        # To avoid 3D array in "lines"
        l = self.lines.reshape(len(self.lines), -1)

        # Sorts to get the adjacent border lines together in the image
        s = l[np.argsort(l[:, 1])]

        for i in range(0, len(s)):
            if (i % 2 == 0):
                # Accessing the pixel values by its row and columns
                points = self.converted_img[((s[i][1]) - offset): ((s[i + 1][3]) + offset),
                         s[i][0]: s[i + 1][2]]  # points = img1[y1:y2, x1:x2] Eg:[168:190, 16:148]

                # Their respective median and mean
                n = (len(s)) / 2
                m1 = np.mean(points)
                m2 = np.median(points)
                self.mean.append(m1)
                self.median.append(m2)
        print("Median of the", n, "lines:", self.mean)
        print("Mean of the", n, "lines:", self.median)

    # Datatable for median and mean of selected image
    def datatable(self, *args):
        self.table = MDDataTable(pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(1, 0.95),
                                 use_pagination=True,
                                 check=True,
                                 rows_num=10,
                                 column_data=[("File name", dp(70)),
                                              ("Lines", dp(20)),
                                              ("Mean", dp(40)),
                                              ("Median", dp(30))],
                                 row_data=[(os.path.basename(self.file_path),
                                            f"{j + 1}",
                                            self.mean[j],
                                            self.median[j])
                                           for j in range(int(len(self.lines) / 2))],
                                 )

        self.table.bind(on_row_press=self.on_row_press)
        self.table.bind(on_check_press=self.on_check_press)
        self.ids.body.add_widget(self.table)

    def on_row_press(self, instance_table, instance_row):
        print(instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        print(instance_table, current_row)

    def download(self, *args):
        # Stores values of first image
        with open("Data Table.csv", 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["File name", "Line", "Median", "Mean"])
            csvwriter.writerows([p for p in
                                 zip([self.file_path.split("/")[-1]] * len(self.median), range(1, len(self.median) + 1),
                                     self.median, self.mean)])


class Assays(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"
        return Tab()


if __name__ == '__main__':
    Assays().run()