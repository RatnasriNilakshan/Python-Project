import requests
city = "Jaffna"

def find_location(city):
    try:
        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid=8d4e7706e24a9f1fc59b0b30b7964887')
        if response.status_code == 200:
            # Extract the weather data from the response
            location_details = response.json()
            longitude = location_details['lon']
            latitude = location_details['lat']

            # Print the response content
            print(longitude, latitude)
        else:
            print('Failed to retrieve location data. Status code:', response.status_code)
    except Exception as e:
        # Connection failed
        print("Connection to failed:", str(e))
find_location(city)