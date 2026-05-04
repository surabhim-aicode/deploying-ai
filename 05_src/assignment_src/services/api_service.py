import requests

class ApiService:

    def get_weather(self, city: str):
        """
        Step 1: Convert city → lat/lon using geocoding API
        Step 2: Fetch weather using Open-Meteo
        Step 3: Transform response into natural language
        """

        # -----------------------------
        # 1. Geocoding API
        # -----------------------------
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1}

        geo_res = requests.get(geo_url, params=geo_params).json()

        if "results" not in geo_res:
            return f"I couldn't find location details for {city}."

        location = geo_res["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        name = location["name"]
        country = location["country"]

        # -----------------------------
        # 2. Weather API
        # -----------------------------
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }

        weather_res = requests.get(weather_url, params=weather_params).json()

        if "current_weather" not in weather_res:
            return "Weather data is currently unavailable."

        current = weather_res["current_weather"]

        temp = current["temperature"]
        wind = current["windspeed"]

        # -----------------------------
        # 3. Transform output into natural language
        # -----------------------------
        return (
            f"Here's the current weather in {name}, {country}: "
            f"The temperature is around {temp}°C with wind speeds of {wind} km/h. "
            f"Overall, it's a fairly typical day weather-wise."
        )