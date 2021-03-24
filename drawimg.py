import inline as inline
import matplotlib
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pyautogui
import time
import os.path
import cv2
import numpy as np
import matplotlib.pyplot as plt

# define the filters for edges
vertical_filter = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
horizontal_filter = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


# function to "draw" edges of image
def draw(name, searchtext):
    # read in the image
    img = plt.imread(name)
    n, m, d = img.shape

    # new image
    edges_img = img.copy()

    # loop over all pixels in the image
    for row in range(3, n - 2):
        for col in range(3, m - 2):
            # filter box and find values
            local_pixels = img[row - 1:row + 2, col - 1:col + 2, 0]

            vertical_transformed_pixels = vertical_filter * local_pixels
            vertical_score = vertical_transformed_pixels.sum() / 4

            horizontal_transformed_pixels = horizontal_filter * local_pixels
            horizontal_score = horizontal_transformed_pixels.sum() / 4

            # combine the horizontal and vertical scores into a total edge score
            edge_score = (vertical_score ** 2 + horizontal_score ** 2) ** .5
            edges_img[row, col] = [edge_score] * 3

    edges_img = 1 - edges_img / edges_img.max()
    for i in range(len(edges_img)):
        for j in range(len(edges_img[i])):
            for k in range(len(edges_img[i][j])):
                if edges_img[i][j][k] < 0.5:
                    edges_img[i][j][k] = 0.5
    # save array as image
    plt.imshow(edges_img)
    plt.imsave(r'C:\file_location\drawing_of_(' + searchtext + ').jpg', edges_img)
    return r'C:\file_location\drawing_of_(' + searchtext + ').jpg'


# download image with searchtext
def download(searchtext):
    # open google images
    url = "https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl"
    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.get(url)

    # search for image
    box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    box.send_keys(searchtext)
    box.send_keys(Keys.ENTER)

    try:
        # download image
        choose = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
        choose.click()
        time.sleep(3)

        actionchains = ActionChains(driver)
        img = driver. \
            find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')

        # context click to "Save As ... "
        actionchains.move_to_element(img).context_click().perform()
        time.sleep(1)
        pyautogui.press('enter')
        pyautogui.press('down', presses=6)
        pyautogui.press('enter')
        time.sleep(3)
        pyautogui.write(r'C:\file_location\(' + searchtext + ').jpg')

        pyautogui.press('enter')
        time.sleep(2)
    except NoSuchElementException:
        temporary = download(searchtext)
        return temporary

    driver.quit()

    if not os.path.exists(r'C:\file_location\(' + searchtext + ').jpg'):
        temporary = download(searchtext)
        return temporary
    else:
        return r'C:\file_location\(' + searchtext + ').jpg'


# clarify contents of image
def denoise(image):
    img = cv2.imread(image)
    dst = cv2.fastNlMeansDenoising(img, None, 9)

    plt.imshow(dst)
    plt.imsave(image, dst)


def main():
    search = input("What do you want to draw? ")
    while True:
        status = input("Cartoon or real? ")
        if status.lower() == "cartoon":
            search = 'cartoon ' + search
            break
        elif status.lower() == "real":
            break
    name = download(search)
    time.sleep(1)
    file = draw(name, search)
    denoise(file)

    return 0


if __name__ == '__main__':
    main()
