import cv2
import csv
import numpy as np
from PIL import Image

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_li, threshold_yen, threshold_otsu, threshold_isodata, threshold_triangle

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.image import Image as CoreImage
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty, StringProperty

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable



Builder.load_file('popup.kv')
Builder.load_file('tabs.kv')

Window.clearcolor = get_color_from_hex("#808080")


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
        #print(self.file_path)

        #self.ids.undetected_image.source = self.file_path


        # check for non-empty list i.e, file selected
        if self.file_path:
            self.ids.get_file.text = self.file_path

            # load the image and into grayscale
            img = cv2.imread(self.file_path)

            #print(type(img))



    #cropping code
    #def cropping(self, selection):
        #pass



        # convert image into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold the image to reveal white regions in the image
        thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)[1]

        # find the edges in the image using canny detector(binary image)
        edges = cv2.Canny(thresh, 100, 200)

        # Detect points that form "border lines" of the line
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=100)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        n = len(lines)/2
        #print(ln)


        #img1 = np.array2string(img)
        #print(type(img1))
        #self.ids.detected_image.source = img1
        self.ids.detected_image.source = self.file_path

        self.ids.lines.text = f'{n}'



    def spinner_clicked(self, value):
        global conversion
        def conversionMethod(conv):
            if conv == "Gray":
                return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif conv == "Luminance":
                return rgb2gray(img)
            elif conv == "Red":
                print("its red!")
            elif conv == "Green":
                print("its green!")
            elif conv == "Blue":
                print("its blue!")
            else:
                print("Invalid input!")
        conv = value
        conversion = conversionMethod(conv)
        pass



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

            #self.ids.output_label.text = f'Thresholding method you have picked is: {thresh}'
            pass
        else:
            Tab.checks.remove(threshold)
            thresh = ''
            for x in Tab.checks:
                thresh = f'{thresh} {x}'
            pass



    def slide_it(self, *args):
        global l,s

        self.slide_text.text = str(int(args[1]))
        offset = int(args[1])
        #print(offset)

        # to avoid 3D array in "lines"
        l = lines.reshape(len(lines), -1)

        # sorts to get the adjacent border lines together in the image
        s = l[np.argsort(l[:, 1])]

        mean = []
        median = []
        for i in range(0, len(s)):
            if (i % 2 == 0):
                # accessing the pixel values by its row and columns
                points = img[((s[i][1]) - offset):((s[i + 1][3]) + offset), s[i][0]:s[i + 1][2]]  # points = img1[y1:y2, x1:x2] Eg:[168:190, 16:148]

                # Their respective median and mean
                n = (len(s)) / 2
                m1 = np.mean(points)
                m2 = np.median(points)
                mean.append(m1)
                median.append(m2)
        #print("Median of the", n, "lines:", median)
        #print("Mean of the", n, "lines:", mean)

        self.ids.line.text = f'{n}'
        self.ids.median.text = f'{median}'
        self.ids.mean.text = f'{mean}'



    #def download(self, *args):
        # stores values of first image
        #with open("C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\Data Table.csv", 'w') as csvfile:
            #csvwriter = csv.writer(csvfile)
            #csvwriter.writerow(["Median", "Mean"])
            #csvwriter.writerows([p for p in zip(median, mean)])

        # stores values from second image
        #with open("C:\\Users\\annma\\OneDrive\\Desktop\\Assay Project\\Data Table.csv", 'a+') as appendobj:
            #csvappend = csv.writer(appendobj)
            #csvappend.writerows([p for p in zip(median, mean)])


class Assays(App):
    def build(self):
        return Tab()


if __name__ == '__main__':
    Assays().run()





