import os, cookielib, urllib2, re, datetime
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, URLError
from Event import Event

base_url='http://med.stanford.edu/seminars/'

def parse_time(t):
    #5:30 PM 
    t=t.strip()
    res=datetime.datetime.strptime(t,"%I:%M %p")
    
    return res

def parse_day(d):
    #Oct 10, 2013 
    d=d.strip()
    res=datetime.datetime.strptime(d,"%b %d, %Y")
    
    return res


def parse_date(date):
    res=dict()
    udate=date.span.text.strip()
    udate=re.sub("\(.*?\)","",udate)
    
    if('|' in udate):
        #Oct 10, 2013  | 5:30 PM - 6:30 PM
        sdate=udate.split('|')
        day=parse_day(sdate[0])
        times=sdate[1].split("-")
        t_start=parse_time(times[0])
        t_end=parse_time(times[1])
        

            
        
        start=datetime.datetime.combine(day.date(),t_start.time())
        if t_start == t_end:
            end=datetime.datetime.combine(day.date()+datetime.timedelta(1),t_end.time())
        else:
            end=datetime.datetime.combine(day.date(),t_end.time())
        
    else:
        sdate=udate.split('-')
        if sdate[1].strip() != "":
            #Oct 28, 2013  -  Oct 29, 2013 
            start=parse_day(sdate[0])
            delta=datetime.timedelta(1)
            end=parse_day(sdate[1])+delta
        else:
            #Oct 11, 2013  -
            start=parse_day(sdate[0])
            delta=datetime.timedelta(1)
            end=start+delta
    
    
    tag=date.span.next_sibling \
    .replace('|', "") \
    .strip() \
    .replace(', ',',') \
    .replace(' & ',',') \
    .strip() \
    .split(',')
    
    res['tags']=tag
    res['start_time']=start
    res['end_time']=end
    
    return res 
    
def parse_info(info):

    title=info.find('div',class_='eventTitle').text.strip()
    loc=info.find('div',class_='eventText').text.strip()
    loc=re.sub('[\t\n]+',' ',loc)
    link=info.find('a',class_='link_nounderline')

    if link is not None:
        link=link['href']
        if 'http' not in link:
            link=base_url+link
    else:
        link=''
    res={}
    res['title']=title
    res['location']=loc
    res['link']=link
    
    return res
    
def make_event(d):
    d['department']=",".join(d['tags'])
    d['speaker']=""
    d['description']=""
    d['start_time']=d['start_time'].strftime("%Y-%m-%dT%H:%M")
    d['end_time']=d['end_time'].strftime("%Y-%m-%dT%H:%M")
    
    res=Event.from_dict(d)
    
    return(res)
    
    
    
def get_events():

    COOKIEFILE = 'cookies_med.lwp'
    user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    
    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        # if we have a cookie file already saved
        # then load the cookies into the Cookie Jar
        cj.load(COOKIEFILE)
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    
    
    try:
        headers = { 'User-Agent' : user_agent }
        req = Request(base_url+'upcomingEvents.do',None,headers)
        response = urlopen(req)
    except URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        #pass
    except Exception,e:
        print e
    
    soup = BeautifulSoup(response.read())  
    event_list=soup.find('div',id='eventSection')
    date_list=event_list.find_all('div',class_='dateline')
    info_list=event_list.find_all('div',class_='eventInfo')
    output=[]
    
    for date,info in zip(date_list,info_list):
        res1=parse_date(date)
        res2=parse_info(info)
        res=dict(res1.items() + res2.items())
        e=make_event(res)
        output.append(e)
        
    return(output)
