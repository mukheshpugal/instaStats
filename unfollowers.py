from selenium import webdriver
import time
from creds import getCreds

credentials = getCreds()

drv = webdriver.Chrome()
drv.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
drv.implicitly_wait(3)

# Login
drv.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(credentials['username'])
drv.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(credentials['password'])
drv.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()

# Don't save login
drv.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()

# Turn off notifications
drv.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()

drv.get('https://www.instagram.com/' + uname)
