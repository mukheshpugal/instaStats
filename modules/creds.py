def getCreds():
	import getpass
	import os
	import json

	CREDENTIALS_PATH = os.path.dirname(__file__) + '\\..\\files\\credentials.json'

	if os.path.exists(CREDENTIALS_PATH):
		if input('Load saved credentials? [Y/n] ') in ('Y', 'y', '', 'yes'):
			with open(CREDENTIALS_PATH) as json_file: 
				credentials = json.load(json_file)
	if 'credentials' not in locals():
		credentials = {}
		credentials['username'] = input("Phone number, username or email: ")
		credentials['password'] = getpass.getpass()

		if input('Save credentials? [Y/n]') in ('Y', 'y', '', 'yes'):
			with open(CREDENTIALS_PATH, 'w') as fp:
			    json.dump(credentials, fp)

	return credentials
	