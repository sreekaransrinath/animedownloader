# import requests
# from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as mcon

driver_path = "/usr/local/bin/chromedriver"
chrome_path = "/usr/bin/google-chrome"
option = webdriver.ChromeOptions()
option.binary_location = chrome_path
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

kb = Controller()
m = mcon()
# driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://animepahe.com/anime/nanatsu-no-taizai")
time.sleep(5)
elements = driver.find_elements_by_class_name('episode-wrap.col-12.col-sm-4') # There are x number of elements in this class, each representing one episode thumbnail

for e in elements:
    time.sleep(1)
    ActionChains(driver).move_to_element(e).key_down(Keys.CONTROL).click(e).key_up(Keys.CONTROL).perform() #Open link in new tab

    #Move to next tab
    kb.press(Key.ctrl)
    kb.press(Key.tab)
    kb.release(Key.tab)
    kb.release(Key.ctrl)
    time.sleep(1)

    if driver.title.find('Nanatsu') == -1: #Detect popup
        time.sleep(1.5)
        # kb.press(Key.alt)
        # kb.press(Key.f4)
        # kb.release(Key.f4)
        # kb.release(Key.alt)
        driver.close()
        time.sleep(1)

    downloaddropdown = driver.find_element_by_id('downloadMenu') #This is the Download Dropdown button that reveals resolution selector
    
    # downloaddropdown = driver.find_element_by_partial_link_text('Download') #This is the Download Dropdown button that reveals resolution selector
    downloaddropdown.click()
    time.sleep(1)

    if driver.title.find('Nanatsu') == -1: #Detect popup
        time.sleep(1.5)
        # kb.press(Key.alt)
        # kb.press(Key.f4)
        # kb.release(Key.f4)
        # kb.release(Key.alt)
        driver.close()
        time.sleep(1)

    res_select = driver.find_element_by_partial_link_text(' 1080p (') #Resolution Select Button. Select 1080p or 720p
    res_select.click()
    time.sleep(1)
    
    if (driver.title.find('Nanatsu') == -1) and (driver.title.find('Shrink your URL') == -1): #Detect popup
        time.sleep(1.5)
        # kb.press(Key.alt)
        # kb.press(Key.f4)
        # kb.release(Key.f4)
        # kb.release(Key.alt)
        driver.close()
        
    if driver.title.find('Shrink your URL') != -1: #Check if this is the Adfly page before clicking the Skip ad button
        time.sleep(20)
        m.position = (1266, 161) #Coordinates of Skip Ad button in Adfly page 
        m.click()
        time.sleep(1)

    if (driver.title.find('AnimePahe') == -1) and (driver.title.find('Shrink your URL') == -1): #Detect popup
        time.sleep(1.5)
        # kb.press(Key.alt)
        # kb.press(Key.f4)
        # kb.release(Key.f4)
        # kb.release(Key.alt)
        driver.close()
        time.sleep(1)

    if driver.title.find('AnimePahe') != -1: #Check if this is the final download page
        m.position = (729, 399) #Random spot in final page. Click this to trigger popup
        m.click()
        download_button = driver.find_element_by_partial_link_text('Click Here to Download')
        download_button.click()
        time.sleep(2)

        kb.press(Key.ctrl)
        kb.press('w')
        kb.release('w')
        kb.release(Key.ctrl)
        time.sleep(.1)
        kb.press(Key.ctrl)
        kb.press('w')
        kb.release('w')
        kb.release(Key.ctrl)
        time.sleep(.1)
        kb.press(Key.ctrl)
        kb.press('w')
        kb.release('w')
        kb.release(Key.ctrl)

driver.quit()

#Procedure
#do one altf4 after clicking download and waiting 1.5 sec; then click that 1080p button find by text contained; wait 20 secs; click skip ad; wait 1.5 sec then do another alt f4; now find download button by using the text click here to download to identify it and click; then wait 1.5 sec and another altf4; now click download again; now close tab 3 times

# def closewindow():
#     kb.press(Key.alt)
#     kb.press(Key.f4)
#     kb.release(Key.f4)
#     kb.release(Key.alt)

# def nexttab():
#     kb.press(Key.ctrl)
#     kb.press(Key.tab)
#     kb.release(Key.tab)
#     kb.release(Key.ctrl)

# def closetab():
#     kb.press(Key.ctrl)
#     kb.press('w')
#     kb.release('w')
#     kb.release(Key.ctrl)