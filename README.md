# DrawImage  - program draws image from a single word
### Note: webdriver is catered to google chrome and desktop nagivation is catered to windows
### Of course, contents can be motified to be adopted to different webdrivers and OS
This program takes a word as input then asks the user if they want the drawing to be cartoon or real. With the search word, the program opens as webdriver and downloads an image through google images. The program then detects the edges within the downloaded image and writes the edges onto a different file. Finally, the new "drawing" file will go through a denoising function to create a clearer picture. This final result is the "drawing" of the search word input.

# For use: 
### - select file to save images to and insert into "file_location" in script
### - possible need to modify webdriver and desktop navigation

# Process
The Python library Selenium is used for the downloading process from google images. With Selenium and pyautogui, this script is able to navigate through a webdriver and windows desktop.  To detect edges of image and write to new file, Matplotpy is used to access and filter through the RBG values as an array of numbers. OpenCV using cv2 is then applied to denoise the image.
