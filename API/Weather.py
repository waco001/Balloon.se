import requests, json
def getWeatherFromCo(lat,long):
	url = "http://api.wunderground.com/api/08ba7f8e126383f5/conditions/geolookup/q/" + str(lat) + "," + str(long) + ".json"
	print(url)
	print("#################")
	r = requests.get(url)
	jsondata = json.loads(r.text)
	
	data = {

	}
	data['error']=""
	if 'error' in jsondata['response']:
		data['error'] = jsondata['response']['error']['description']
	else:
		data['wind_degrees'] = jsondata['current_observation']['wind_degrees']
		data['wind_dir'] = jsondata['current_observation']['wind_dir']
		data['wind_mph'] = jsondata['current_observation']['wind_mph']
		data['wind_gust_mph'] = jsondata['current_observation']['wind_gust_mph']
		data['wind_string'] = jsondata['current_observation']['wind_string']
		data['location'] = jsondata['current_observation']['display_location']['full']
	return data