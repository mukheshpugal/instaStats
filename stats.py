from selenium import webdriver
import webbrowser
import json
import os

from modules.creds import getCreds
from modules.login import login
from modules.get_users import getUsers

if __name__ == '__main__':

	credentials = getCreds()
	driver = webdriver.Chrome()

	login(driver, credentials)
	
	credentials['username'] = driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').get_attribute('alt').split("'")[0]
	driver.get('https://www.instagram.com/' + credentials['username'])

	followers, varId = getUsers(driver, 'followers')
	following, _ = getUsers(driver, 'following', varId)

	infoDict = {}

	for person in followers + following:
		infoDict[person[0]] = person[1:]

	followers = [f[0] for f in followers]
	following = [f[0] for f in following]

	youFollow = [a for a in following if a not in followers]
	theyFollow = [a for a in followers if a not in following]
	unfollowers = []

	if os.path.exists('./files/oldFollowers.json'):
		with open('./files/oldFollowers.json') as fp:
			oldFollowers = json.load(fp)
		unfollowers = [a for a in oldFollowers if a not in followers]
		with open('./files/oldUnfollowers.json', 'w') as fp:
			json.dump(unfollowers, fp)

	with open('./files/oldFollowers.json', 'w') as fp:
		json.dump(followers, fp)

	if os.path.exists('./files/info.json'):
		with open('./files/info.json') as fp:
			oldDict = json.load(fp)
		for person in unfollowers:
			infoDict[person] = oldDict[person]

	with open('./files/info.json', 'w') as fp: 
		json.dump(infoDict, fp)

	def writeList(name:str):
		with open('./files/' + name + '.js', 'w') as fp:
			fp.write('var ' + name + ' = ')
			json.dump(globals()[name], fp)
			fp.write(';')

	for listname in ('youFollow', 'theyFollow', 'unfollowers', 'infoDict'):
		writeList(listname)

	driver.quit()
	webbrowser.open('stats.html')
