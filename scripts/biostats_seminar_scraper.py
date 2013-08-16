import os, cookielib, urllib2, re, datetime
from urllib2 import Request, urlopen, URLError
from bs4 import BeautifulSoup
import html5lib
from Event import Event

def get_events():
	base_url = 'http://med.stanford.edu/biostatistics/workshop.html'
	
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
		req = Request(base_url,None,headers)
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
	
	biostats_soup = BeautifulSoup(response.read())  
	
	events = []
	location = 'MSOB X-303'
	for speaker in biostats_soup.find_all("div", class_="speaker"):
		#print speaker.string
		#print "speaker", speaker
		#print "parent", speaker.parent
		#print "parent.parent", speaker.parent.parent
		#print "parent.previous_element", speaker.parent.previous_element
		block = speaker.parent.parent
		#date = speaker.parent.previous_sibling.string
		#print block, block
		#print
		date = block.contents[1]
		#print "date", date
		[month, day] = date.string.split('/')
		#print month, day
		if(len(month) == 1):
			month = '0' + month
		if(len(day) == 1):
			day = '0' + day
		full_date = '2013-' + month + '-' + day + 'T'
		start = full_date + '13:15'
		end = full_date + '15:00'
		#print 'department?', block.contents[3]
		department = ''
		for child in speaker.parent.contents[2].children:
			#print 'child', child
			#print 'type(child)', type(child)
			#print 'child.string', child.string
			#print 'type(child.string)', type(child.string)
			if child.string is not None:
				department = department + ', ' + child.string.strip()
		department = department[2:]
		if department == '':
			continue
		meta = block.contents[5]
		title = meta.contents[0].contents[0]
		#meta = speaker.parent.next_sibling
		#title = meta.contents[0].string
		link = meta.a['href']
		events.append(Event(start, end, department, speaker.text, title, '', location, [], link))
	return(events)

#for speaker in biostats_soup.find_all("div", class_="speaker"):
#	speaker.string
#for credentials in biostats_soup.find_all("div", class_="credientials"):
#	credentials.string
#for title in biostats_soup.find_all("div", class_="title"):
#	title.string
