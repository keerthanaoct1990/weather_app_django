import requests
import datetime
from django.shortcuts import render


def index(request):
	API_KEY = '604fc7f16a5d8405923ad2c39786e034'
	current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'
	forecast_weather_url = 'https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

	if request.method == 'POST':
		city1 = request.POST['city1']
		city22 = request.POST.get('city2', None) #city2 is not mandatory. If city2 field is empty value is None
		weather_data1, forecast_data1 = get_current_forecast_weather(city1, API_KEY, current_weather_url, forecast_weather_url)

		if city22:
			weather_data2, forecast_data2 = get_current_forecast_weather(city22, API_KEY, current_weather_url, forecast_weather_url)
		else:
			weather_data2, forecast_data2 = None, None

		context = {
		'weather_data1' : weather_data1,
		'forecast_data1' : forecast_data1,
		'weather_data2' : weather_data2,
		'forecast_data2' : forecast_data2
		}

		return render(request, 'weather_app/index.html', context)

	else:
		return render(request, 'weather_app/index.html')


#This function retrives the current weather data and forecast weather using lat and lon extracted from current data
def get_current_forecast_weather(city, api_key, current_weather_url, forecast_weather_url): 
	response = requests.get(current_weather_url.format(city, api_key)).json()
	lat, lon = response['coord']['lat'], response['coord']['lon']
	forecast_response = requests.get(forecast_weather_url.format(lat, lon, api_key)).json()

	weather_data = {
		'city': city,
		'temperature' : round(response['main']['temp'] - 273.15, 2),
		'description' : response['weather'][0]['description'],
		'icon'        : response['weather'][0]['icon']

	}

	daily_forecasts = []
	for daily_data in forecast_response['daily'][:5]:
		daily_forecasts.append({
			'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
			'min_temp' : round(daily_data['temp']['min'] - 273.15, 2),
			'max_temp' : round(daily_data['temp']['max'] - 273.15, 2),	
			'description' : daily_data['weather'][0]['description'],	
			'icon' : daily_data['weather'][0]['icon']
		})

	return weather_data, daily_forecasts
