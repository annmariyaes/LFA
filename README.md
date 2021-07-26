
# LFA Python App

A readme for the python-based Application that analyse the Lateral Flow Assay images and quantify their bands/spots.


## Description

The LFA Python App consists of mainly 3 tabs:

1. **_Band automatic detection_** which works mainly with the help of Hough line transform using OpenCV package

2. **_Background correction_** with different color conversion and thresholding methods.

3. **_Intensity data_** which creates datatable containing details like number of bands in that image and their respective mean and median. 


## Creating Virtual Environment

1. Open the directory: 
   
   Windows/Unix/macOS: ```cd LFAApp_git```
   

2. In order to create the new virtual environment enter the command:
   
   Windows: ```python -m venv project_env```
   
   Unix/macOS: ```python3 -m venv project_env```
   
    This will create a new virtual environment named “project_env”.


3. Once the environment is created, you can activate the environment using the command:
   
   Windows: ```project_env\Scripts\activate.bat```
   
   Unix/macOS: ```project_env/bin/activate```
   

4. Use requirements.txt file for a new person to install all dependencies.
      
   Windows: ```pip install -r /path/to/requirements.txt```
   
   Unix/macOS: ```python3 -m pip install -r requirements.txt```
   
   To check, if all the packages and dependencies are successfully installed, use the command: 
   Windows/Unix/macOS: ```pip freeze```
   

5. To deactivate the directory:

   Windows/Unix/macOS: ```deactivate```


6. To delete or remove directory:
   
   Windows: ```rmdir project_env /s```
   
   Unix/macOS: ```rm -r project_env```


## User's Guide

After installing the packages, run the main.py code.

In the first tab, firstly upload the LFA image from your folder. 
Then hit the "Apply Crop" button, which opens up a ROI window, crop the image without including the shadow regions. 
Again a new window popups up. Close both windows and return to the LFA app. 
Next hit the "Apply detection" button, then the app displays the cropped band-detected image and also the in the next box the number of lines detected from that image.

<img width="401" alt="tab1" src="https://user-images.githubusercontent.com/75450699/126910016-53381149-5168-4d83-8bbb-68d053a26819.png">


Coming to the second tab, select the color conversion method from the dropdown options(Gray, Luminance, Red, Green, Blue).
Then select any thresholding methods like OTSU, Li, Yen, Isodata, Triangle.
For increasing the area for the better calculation of median and mean of the image, set an offset value(preferably 20).

<img width="401" alt="tab2" src="https://user-images.githubusercontent.com/75450699/126910029-728126ed-a904-4e8e-9500-f3e507ffbeb1.png">


In the last tab, click "Create datatable" button, which will turn to a datatable containing intensity data and other related details of the detected-bands.
Lastly download datatable, if you want to store the information of the uploaded image. 

<img width="401" alt="tab3" src="https://user-images.githubusercontent.com/75450699/126910032-fde9ad71-17ec-4f77-ac25-11993e6a6f8a.png">

 
