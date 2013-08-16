import urllib2
#bs4 contains beautifulsoup4
import bs4
#import our own Event package for the calendar
import Event
#using html5 instead of the standard beautiful soup html library
import html5lib
import datetime
import string


def get_events():
    site = 'http://cancer.stanford.edu/patient_care/services/multidisciplinaryTumorBoard.html'

    siteXML = bs4.BeautifulSoup(urllib2.urlopen(site),"html5lib")

    #we know that this simple site just stores the dates and meetings in tables

    siteXMLTables = siteXML.find_all('table')

    #for this site we only need the first table

    #now go down the tree and get each Tr tag..

    siteXMLTablesTrTags = siteXMLTables[0].find_all('tr')

    #first table section is just tages
    today = datetime.date.today()
    todaysWeekday=datetime.datetime.now().weekday()
    dayNumberLibrary = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];

    events=[]

    for t in siteXMLTablesTrTags:

        #0th tag isn't an actual event.
        if t.find('td').getText() == "Tumor Board":
            #go back to top of loop
            continue
        
        department = t.find_all('td')[0].getText()
        description = t.find_all('td')[3].getText()
        title = department + " Tumor Boards"
        seminarDay = t.find_all('td')[1].getText()
        
        #if seminar day isn't weekly...just skip
        if(seminarDay not in dayNumberLibrary):
            continue
        
        startEndTime = t.find_all('td')[2].getText().replace(" ","")
        #some have noon and not 12:00pm in them...
        startEndTime = startEndTime.replace("noon",":00pm")
        startEndTime = startEndTime.split("-")
        start_time = datetime.datetime.strptime(startEndTime[0],"%I:%M%p")
        start_time = start_time.time()
        end_time = datetime.datetime.strptime(startEndTime[1],"%I:%M%p")
        end_time = end_time.time()
        seminarDay = dayNumberLibrary.index(seminarDay)
        dayDelta= seminarDay-todaysWeekday

        #get the next 4 weeks
      
        for week in range(4):
            nextWeekday = today+ datetime.timedelta(days=dayDelta,weeks=week)
            nextWeekdayStart = datetime.datetime.combine(nextWeekday,start_time)
            nextWeekdayEnd = datetime.datetime.combine(nextWeekday,end_time)
            nextWeekdayStart= nextWeekdayStart.strftime("%Y-%m-%dT%H:%M")
            nextWeekdayEnd= nextWeekdayEnd.strftime("%Y-%m-%dT%H:%M")       
            events.append(Event.Event(start_time=nextWeekdayStart,end_time=nextWeekdayEnd,department=department,title=title,description=description))
            

    return events

     

        
