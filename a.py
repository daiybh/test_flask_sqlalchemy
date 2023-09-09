import requests

for a in range(0,11):
    b =int((a+3)/4)
    print(a,b)
data={"name":"xyz","email":"aa@aa.com"} 


response=requests.post("http://127.0.0.1:5000/users",json=data)
print(response.json())


response=requests.post("http://127.0.0.1:5000/leds",json=data)
print(response.json())