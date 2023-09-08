
This is a Flask app demo.

This demo use sqlite as database.

on frist run this app , need create database ,call api "http://127.0.0.1:5000/index/createdb"

then can enjoy it.

curl -X POST -H "Content-Type: application/json"  -data {'name':'aa','email':'aa@aa.com'} http://127.0.0.1:5000/users



curl --header "Content-Type: application/json"  --request POST   --data '{"name":"xyz","email":"aa@aa.com"}' 
 http://127.0.0.1:5000/users