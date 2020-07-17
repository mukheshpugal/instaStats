from selenium import webdriver
import json

from modules.creds import getCreds
from modules.login import login
from modules.get_users import getUsers

if __name__ == '__main__':

	credentials = getCreds()
	driver = webdriver.Chrome()

	login(driver, credentials)
	driver.get('https://www.instagram.com/' + credentials['username'])

	followers, varId = getUsers(driver, 'followers')
	following, _ = getUsers(driver, 'following', varId)

	# infoDict = {}

	# for person in followers + following:
	# 	infoDict[person[0]] = person[1:]

	# with open('info.json', 'w') as fp: 
	# 	json.dump(infoDict, fp)