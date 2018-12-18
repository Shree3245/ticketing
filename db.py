from mongoengine import *
connect('mongoengine_test', host='localhost', port=27017)
from pprint import pprint
import datetime
now = datetime.datetime.now()

class Ticket(Document):
    ticketID = StringField(required=True, max_length=200)
    uID = StringField(required=True, max_length=500)
    toID = StringField(required=True, max_length=5000)
    ticket = StringField(required=True, max_length=20000)
    ticketSubect= StringField(required=True, max_length=1000)
    situation=StringField(default = "Not Yet Completed")
    published = DateTimeField(default=now)

def ticketInsert(ticketNum,UID,TID,ticket,subject):
    #print(ticketNum,UID,TID,ticket,subject)
    ticketNum=Ticket(
        ticketID=(ticketNum),
        uID=(UID),
        toID=(TID),
        ticketSubect=(subject),
        ticket=(ticket),         
    )
    ticketNum.save()       # This will perform an insert
    

def complete(ticketNum):
    temp = Ticket.objects.get(ticketID=ticketNum)
    temp.situation="Completed"
    temp.save()

def find(user):


    temp = Ticket.objects(uID=user)
    x=temp.to_json()
    
    pprint("{}".format(x))

#Ticket.objects(uID='5a70b5731855790c9322fe4b').delete()
