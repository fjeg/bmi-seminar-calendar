from datetime import datetime

import vobject

defaults = {}
defaults['start_time']=''
defaults['end_time']=''
defaults['department']=''
defaults['speaker']=''
defaults['title']=''
defaults['description']=''
defaults['location']=''
defaults['tags']=[]
defaults['link']=''

class Event():


    def __init__(self,
            start_time=defaults['start_time'],
            end_time=defaults['end_time'],
            department=defaults['department'],
            speaker=defaults['speaker'],
            title=defaults['title'],
            description=defaults['description'],
            location=defaults['location'],
            tags=defaults['tags'],
            link=defaults['link']):
        """
        UTC STANDARD http://www.w3.org/TR/NOTE-datetime
        start_time:    YYYY-MM-DDThh:mmTZD
        end_time:    YYYY-MM-DDThh:mmTZD
        department:    Department putting on the talk
        speaker:    name of speaker
        title:    Title of talk
        description:    description of the talk given by site
        tags: a list of strings indicating tags
        """
        self.start_time = start_time #datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        self.end_time = end_time #datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
        self.department = department
        self.speaker = speaker
        self.title = title
        self.description = description
        self.location = location
        self.tags = tags
        self.link = link
    

    # input: dictionary of attributes to construct an event
    @classmethod
    def from_dict(cls,d):
        event = cls(
                d.get('start_time',defaults['start_time']), 
                d.get('end_time',defaults['end_time']), 
                d.get('department',defaults['department']), 
                d.get('speaker',defaults['speaker']),
                d.get('title',defaults['title']),
                d.get('description',defaults['description']),
                d.get('location',defaults['location']),
                d.get('tags',defaults['tags']),
                d.get('link',defaults['link']))
        return event


    def get_fmt_start_date(self,fmt_string):
        start_stamp = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
        return start_stamp.strftime(fmt_string)

    def get_fmt_end_date(self,fmt_string):
        end_stamp = datetime.strptime(self.end_time, '%Y-%m-%dT%H:%M')
        return end_stamp.strftime(fmt_string)
        

    def __unicode__(self):
        s = ''
        s+='start_time:\t' + self.start_time + u'\n'
        s+='end_time:\t' + self.end_time + u'\n'
        s+='department:\t' + self.department + u'\n'
        s+='speaker:\t' + self.speaker + u'\n'
        s+='title:\t' + self.title + u'\n'
        s+='description:\t' + self.description + u'\n'
        s+='location:\t' + self.location + u'\n'
        s+='tags:\t' + ','.join(self.tags) + u'\n'
        s+='link:\t' + self.link + u'\n'
        return s
    
    def __str__(self,encoding="utf-8"):
        s = self.__unicode__().encode(encoding)
        return s


    def __cmp__(self,other):
        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')

        if d1 < d2:
            return -1
        elif d1 == d2:
            return 0
        else: # d1 > d2
            return 1


    # comparison operators
#    def __eq__(self,other):
#        """
#        return ((self.start_time == other.start_time) and
#                (self.location == other.location) )
#        """
#        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
#        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')
#        return d1==d2
#
#    def __ne__(self,other):
#        """
#        return ((self.start_time != other.start_time) or
#                (self.location != other.location) )
#        """
#        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
#        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')
#        return d1!=d2
#
#    def __lt__(self,other):
#        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
#        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')
#        return d1 < d2
#
#    def __le__(self,other):
#        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
#        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')
#        return d1 <= d2
#
#    def __gt__(self,other):
#        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
#        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')
#        return d1 > d2
#
#    def __ge__(self,other):
#        d1 = datetime.strptime(self.start_time, '%Y-%m-%dT%H:%M')
#        d2 = datetime.strptime(other.start_time, '%Y-%m-%dT%H:%M')
#        return d1 >= d2
    
    def isFranciscoDreamy(self):
        print 'yes, when freshly showered'

    #input a list of events
    #returns a string that represents an ical object. 
    #Write it to a file if you so desire :-)
    @staticmethod
    def to_ics(events):
        cal = vobject.iCalendar()
        for e in events:
            elem=cal.add('vevent')
            elem.add('summary').value=e.title
            desc ="" 
            desc+="Speaker: " + e.speaker +"\n\n" 
            desc+="Department: " + e.department + "\n\n"
            desc+="Tags: " + ", ".join(e.tags) + "\n\n"
            desc+="Description: " + e.description + "\n\n"
            desc+="Link: " + str(e.link) + "\n"
            elem.add('description').value=desc
            st=datetime.strptime(e.start_time, '%Y-%m-%dT%H:%M')
            en=datetime.strptime(e.end_time, '%Y-%m-%dT%H:%M')
            elem.add('dtstart').value=st
            elem.add('dtend').value=en
            elem.add('location').value=e.location
        return cal.serialize()
        
    def to_google(self,api_key):
        pass

