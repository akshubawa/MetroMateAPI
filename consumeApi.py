import requests

def encode(string):
    return string.replace(" ", "%20")

source = input("Enter source: ")
source = encode(source)
destination = input("Enter destination: ")
destination = encode(destination)

response = requests.get(f"http://127.0.0.1:8000/route?source={source}&destination={destination}")
output = response.json()
print(output)