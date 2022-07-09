from selenium import webdriver   
from selenium.webdriver.common.by import By   
from selenium.common.exceptions import NoSuchElementException
import cv2
from pytesseract import image_to_string
import os
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
browser = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
browser.get('https://www.amazon.com/errors/validateCaptcha')

while True:
    # time.sleep(1)
    try:
        captchaImage = browser.find_element(By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img').screenshot_as_png
        with open('status.png', 'wb') as f:
                f.write(captchaImage)

        img = cv2.imread("./status.png")
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (h, w) = gry.shape[:2]
        gry = cv2.resize(gry, (w*2, h*2))
        cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
        thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        txt = image_to_string(thr)        

        os.system("rm status.png")

        inputBox = browser.find_element(By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/input')
        inputBox.send_keys(txt)

        submit = browser.find_element(By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
        submit.click()
    except:
        break

    
    