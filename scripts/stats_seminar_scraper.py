import urllib2
from bs4 import BeautifulSoup
from Event import Event

"""
with open('stats_source.html') as f:
    s = ''.join(f.readlines())
seminar_html = BeautifulSoup(s)
"""

def get_events():
    stats_seminar_url = 'http://www-stat.stanford.edu/seminars/stat/index.html'
    seminar_html = BeautifulSoup(urllib2.urlopen(stats_seminar_url),'html5lib')
    headlines = seminar_html.find_all('strong',class_='headline')

    location = 'Sequoia 200'
    start_HH = '15'
    start_MM = '45'
    end_HH = '17'
    end_MM = '15'
    department = 'Statistics'

    event_list = []

    for headline in headlines:
        month,YYYY = headline.string.split()
        table = headline.find_next_sibling('table')

        institutions = table.find_all(class_='dataCell1i') #hack to find each entry cell
        for institution in institutions:
            event_html = institution.parent
            event_entries = event_html.find_all('td')

            if '---' in event_entries[3].get_text():
                continue

            event_dict = {}

            # date time
            MM,DD = event_entries[0].get_text()[:5].split('.')
            event_dict['start_time'] = YYYY + '-' + MM + '-' + DD + 'T' + start_HH + ':' + start_MM
            event_dict['end_time'] = YYYY + '-' + MM + '-' + DD + 'T' + end_HH + ':' + end_MM

            event_dict['department'] = department
            event_dict['speaker'] = event_entries[1].get_text()
            event_dict['title'] = event_entries[3].get_text()
            event_dict['description'] = ''
            event_dict['location'] = location
            event_dict['tags'] = []
            event_dict['link'] = event_entries[4].find('a')['href']

            event = Event.from_dict(event_dict)
            event_list.append(event)

    return event_list


"""
how the html works right now:

<strong class="headline"><a name="jul">July 2013</a></strong>
<br>
<img src="../../inc/img/shim.gif" width="1" height="5" alt="" border="0">
<br>
<table>
    <tr>
        <td class="titleCell">Date</td>
        <td class="titleCell">Speaker</td>
        <td class="titleCell">Affiliation</td>
        <td class="titleCell">Title</td>
        <td class="titleCell">Abstract</td>
    </tr>

    <tr>
         <td class="dataCell0">MM.DD</td>
         <td class="dataCell">first last</td>
         <td class="dataCell1i">institution</td>
         <td class="dataCell">title</td>
         <td class="dataCell0"><a href="PDFURL"><img useless image></a></td>
     </tr>
 </table>
 """
        



