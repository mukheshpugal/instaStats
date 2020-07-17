from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

def login(driver, credentials):
	print("Loading page...")
	driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
	driver.implicitly_wait(5)

	# Login
	print("Logging in...")
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(credentials['username'])
	driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(credentials['password'])

	try:
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
	except ElementClickInterceptedException:
		print("Wrong password")
		finish()

	# Don't save login
	try:
		driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
	except NoSuchElementException:
		if driver.current_url == 'https://www.instagram.com/accounts/login/?source=auth_switcher':
			print("Wrong password")
			finish()

	
	driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()

	print("Logged in successfully.")
	return driver
	