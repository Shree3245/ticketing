import requests
import json
import db

def authenticate(username,password):
    url = "http://test.greenkogroup.com/gomstest/api/auth/login"
    test = requests.post(url,auth=(username,password))
    json_data = json.loads(test.text)
    output =  json_data['status'].lower()

    global uID
    uID = '0'
    try:
        uID=str(json_data['data']['userId'])
    except KeyError:
        pass
    return output,uID



"""auth ="start" 
while auth != 'success':
    username = input("Username: ")
    password = input("Password: ")
    try:
        auth = authenticate(username,password)
    except KeyError:
        pass

while True:
    home = input("Would you like to issue a token/ see all issued tokens: (I/S): ")
    home.lower()
    if home =='i':
        tUser = str(input('Issue to: '))
        subject = str(input("Issue pertaining to: \n"))
        ticket = str(input("What is the issue: \n"))

        db.ticketInsert("1",uID,tUser,ticket,subject)

    elif home == 's':
        db.find(uID)"""