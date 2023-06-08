import requests

data={"name":"xyz","email":"aa@aa.com"} 


response=requests.post("http://127.0.0.1:5000/users",json=data)
print(response.json())