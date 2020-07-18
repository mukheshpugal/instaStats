import json
def getUsers(driver, userType, varId=None):

	variables = {}
	if varId is None:
		try:
			variables["id"] = driver.execute_script("return window.__additionalData[Object.keys(window.__additionalData)[0]].data." "graphql.user.id")
		except:
			variables["id"] = driver.execute_script("return window._sharedData." "entry_data.ProfilePage[0]." "graphql.user.id")

	else:
		variables['id'] = varId
	variables['first'] = 50
	followlist = []

	if userType == 'followers':
		query_hash = '37479f2b8209594dde7facb0d904896a'
	elif userType == 'following':
		query_hash = '58712303d941c6855d4e888c5f0cd22f'
	else:
		return

	grapgql = 'view-source:https://www.instagram.com/graphql/query/?query_hash=' + query_hash

	edge = 'edge_followed_by' if userType == 'followers' else 'edge_follow'

	done = 0
	while True:
		url = grapgql + f'&variables={json.dumps(variables)}'
		driver.get(url)

		data = json.loads(driver.find_element_by_xpath('/html/body/table/tbody/tr/td[2]').text)["data"]
		nodes = data['user'][edge]['edges']
		done += len(nodes)
		followlist += [(node['node']['username'], node['node']['full_name'], node['node']['profile_pic_url']) for node in nodes]
		print(f'Loaded: {done} {userType}')
		page_info = data['user'][edge]['page_info']
		if not page_info['has_next_page']: break
		variables['after'] = page_info['end_cursor']

	return followlist, variables['id']