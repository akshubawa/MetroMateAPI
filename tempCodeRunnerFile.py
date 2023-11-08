import requests

def encode(string):
    return string.replace(" ", "%20")

source = input("Enter source: ")
source = encode(source)
destination = input("Enter destination: ")
destination = encode(destination)

response = requests.get(f"https://metromate.onrender.com/route?source={source}&destination={destination}")
output = response.json()
print(output)