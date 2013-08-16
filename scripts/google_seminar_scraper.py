import requests
from Event import Event
from datetime import datetime


#CS "forumstanford@gmail.com"
#BMI "0huf8fn26r1fosph2u419gl79s@group.calendar.google.com"



def get_events(calendar_id,dept):
    payload={'key':'AIzaSyBaD1TWdledFcAcgM-zEHT47-ojbNqj5Zo','timeMin':datetime.today().strftime("%Y-%m-%dT%H:%M:00-07:00")}
    base_url="https://www.googleapis.com/calendar/v3"
    query="/calendars/"+calendar_id+"/events"
    events=requests.get(base_url+query, params=payload).json()[u'items']
    output=[]
    #print(events)
    for e in events:
        res={}
        start=e[u'start']
        end=e[u'end']
        if u'dateTime' in start:
            res['start_time']=start[u'dateTime'][:-9]
            res['end_time']=end[u'dateTime'][:-9]
        else:
            res['start_time']=start[u'date']+u'T00:00'
            res['end_time']=end[u'date']+u'T00:00'
            
        res['speaker']=u""
        res['department']=dept
        res['description']=e.get(u'description','')
        res['location']=e.get(u'location','')
        res['title']=e.get(u'summary','')
        res['link']=e.get(u'htmlLink','')
        #print(res)
        output.append(Event.from_dict(res))
        
    return output
