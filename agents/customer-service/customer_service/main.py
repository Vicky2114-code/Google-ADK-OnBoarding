import requests

API_KEY = "b86200d0163cca23818fb666637cfbda33e3cbae"
test_url = f"https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key={API_KEY}"
response = requests.get(test_url)

print("Status Code:", response.status_code)
print("Response:", response.json())
