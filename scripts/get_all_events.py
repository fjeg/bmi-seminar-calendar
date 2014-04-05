import stats_seminar_scraper
import probability_seminar_scraper
import med_seminar_scraper
import google_seminar_scraper
import biostats_seminar_scraper
import tumor_boards_scraper
from Event import Event

import jinja2
from datetime import datetime,timedelta


# Do all necessary scraping
event_list = []
event_list.extend( stats_seminar_scraper.get_events() )
event_list.extend( probability_seminar_scraper.get_events() )
event_list.extend( med_seminar_scraper.get_events() )
event_list.extend( google_seminar_scraper.get_events('forumstanford@gmail.com','CS') )
event_list.extend( google_seminar_scraper.get_events('0huf8fn26r1fosph2u419gl79s@group.calendar.google.com','BMI') )
#event_list.extend( biostats_seminar_scraper.get_events() )
event_list.extend( tumor_boards_scraper.get_events() )
event_list.sort()
cur_event_list = []

# Remove old events
today_date = datetime.now()
for e in event_list:
    start_date = datetime.strptime(e.start_time, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(e.end_time, '%Y-%m-%dT%H:%M')
    if start_date >= today_date:
        cur_event_list.append(e)


#Build webpage from event list
templateLoader = jinja2.FileSystemLoader( searchpath="../templates/" )
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "seminar_page_template.html"
template = templateEnv.get_template( TEMPLATE_FILE )

templateVars = { "event_list" : cur_event_list }
outputText = template.render( templateVars ).encode('utf8')

with open('../WWW/bmi_seminars.ics','w') as ics:
    ics.write(Event.to_ics(cur_event_list))

with open('../WWW/seminar_page.html','w') as f:
    f.write(outputText)

