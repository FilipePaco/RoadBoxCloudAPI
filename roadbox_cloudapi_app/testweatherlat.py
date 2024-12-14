# import required modules
import requests, json

# Enter your API key here
api_key = "c851a04b1a1055e2db0008f82d274a0b"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Enter latitude and longitude
latitude = -16.6199877
longitude = -49.2553911

# complete_url variable to store the full URL
complete_url = f"{base_url}appid={api_key}&lat={latitude}&lon={longitude}"

# get method of requests module to fetch response
response = requests.get(complete_url)

# convert response to JSON
x = response.json()
print(x)

# Check if the request was successful
if x["cod"] == 200:  # HTTP 200 means the request was successful
    y = x.get("main", {})
    current_temperature = y.get("temp", "N/A")
    current_pressure = y.get("pressure", "N/A")
    current_humidity = y.get("humidity", "N/A")
    z = x.get("weather", [{}])
    weather_description = z[0].get("description", "N/A")

    # print the results
    print(" Temperature (in kelvin unit) = " +
          str(current_temperature) +
          "\n atmospheric pressure (in hPa unit) = " +
          str(current_pressure) +
          "\n humidity (in percentage) = " +
          str(current_humidity) +
          "\n description = " +
          str(weather_description))
else:
    print(f"Error: {x.get('message', 'Unknown error')}")
