import requests

url = "http://localhost:8000/predict"
with open("test_digit_7_0.png", "rb") as f:
    response = requests.post(url, files={"file": f})
print(response.json())
