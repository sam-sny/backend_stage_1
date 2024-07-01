from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.get("/api/hello")
async def read_root(visitor_name: str, request: Request):
    client_ip = request.client.host
    location = "New York"  # Placeholder
    temperature = 11  # Placeholder temperature in Celsius

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    return {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
