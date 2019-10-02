import urequests as requests





url_loc = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyA24afb5VJ2UD1Y0sdfvJU2oouGaWzjnAE"

url_weather = "http://api.openweathermap.org/data/2.5/weather?lat=40&lon=-73&appid=874fd32c716aa4cc9496395a12673597"

# sending post request and saving response as response object
r = requests.post(url = url_loc, json = {"key":"value"})

# extract text as json
result = r.json()

'''
{'location': {'lat': 40.8027, 'lng': -73.9713}, 'accuracy': 3161.0}
'''

