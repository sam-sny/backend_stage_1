from fastapi import FastAPI, Request, HTTPException
import requests
import socket

app = FastAPI()

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            ip_data = response.json()
            return ip_data['origin']
        else:
            return None
    except requests.RequestException:
        return None

@app.get("/api/hello")
async def read_root(visitor_name: str, request: Request):
    # Get client's public IP address
    client_ip = get_public_ip()
    if not client_ip:
        raise HTTPException(status_code=500, detail="Failed to retrieve client IP address")

    # Get the location from the IP address
    location_response = requests.get(f"https://ipinfo.io/{client_ip}/json?token=42737c31ba9b41")
    if location_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching location information")

    location_data = location_response.json()
    city = location_data.get("city")

    # Get the coordinates for the city from the weather API
    weather_response = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=f793ffdcb4b0fd674c897a8a317c7c83")
    if weather_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching weather information")

    weather_data = weather_response.json()
    if not isinstance(weather_data, list) or not weather_data:
        raise HTTPException(status_code=500, detail="Unexpected response structure from weather API")

    # Get the coordinates for the first result
    first_result = weather_data[0]
    lat = first_result['lat']
    lon = first_result['lon']

    # Get the weather information using the coordinates
    weather_info_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=f793ffdcb4b0fd674c897a8a317c7c83&units=metric")
    if weather_info_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching weather details")

    weather_info = weather_info_response.json()
    if 'main' not in weather_info or 'temp' not in weather_info['main']:
        raise HTTPException(status_code=500, detail="Unexpected response structure from weather API")

    temperature = weather_info['main']['temp']

    greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}"

    return {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
