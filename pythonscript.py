import sqlite3
import time
import json
import requests


eventbritekey = "<your eventbrite api key here>";

xingapikey = '<your xing events api key here>';
xinghostid = '<user id from xing events>';

picatickey = "<your picatic api key here>";



EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/events/"
XING_URL = "https://www.xing-events.com/api/event/create"
PICATIC_URL = "https://api.picatic.com/v2/event"

conn = sqlite3.connect('events.sqlite')
cur = conn.cursor()
no = 0
cur.execute("SELECT rowid, * FROM product WHERE s=?", (no,))
p = dict()
c=0;
#  name, description, organizer, start date, start time, end date, end time, time zone, location, price, currency, synicated
for row in cur :
    #print(row);
    p[c] = {
    'rowid': row[0],
    'name': row[1],
    'des': row[2],
    'merc': row[3],
    'sdate': row[4],
    'stime': row[5],
    'edate':row[6],
    'etime':row[7],
    'tzone':row[8],
    'loc': row[9],
    'price':row[10],
    'currency':row[11],
    'syn':row[12]}
    c = c+1

print("number of products",len(p))
for i in p :
    #print(i,p[i])
    eventbritedata = {
        'event.name.html': p[i]['name'],
        'event.description.html': p[i]['des'],
        #'event.organizer_id': p[i]['merc'],
        'event.start.utc': p[i]['sdate']+'T'+p[i]['stime']+'Z',
        'event.start.timezone': p[i]['tzone'],
        'event.end.utc': p[i]['edate']+'T'+p[i]['etime']+'Z',
        'event.end.timezone': p[i]['tzone'],
        #'event.venue_id': p[i]['loc'],
        'event.currency': p[i]['currency'],
        'event.invite_only': True,
        'event.shareable': False,
        }

    eventbriteresponse = requests.post(EVENTBRITE_URL, data=eventbritedata, headers = {
        "Authorization": "Bearer "+eventbritekey,
    })
    print(eventbriteresponse.text) #TEXT/HTML
    status = eventbriteresponse.status_code
    print(status)
    if(status == 200):
        yes = 1
        cur.execute("UPDATE product SET s = ? WHERE rowid=?",(yes, p[i]['rowid']))
        print("mark done for row:",p[i]['rowid'])


    xingeventsparams = {
        'apikey' : xingapikey,
        'hostId': xinghostid,
        'title' : p[i]['name'],
        'country' : 'US',
        'selectedDate' : p[i]['sdate']+'T'+p[i]['stime'],
        'selectedEndDate' : p[i]['edate']+'T'+p[i]['etime'],
        'description' : p[i]['des'],
        'timezone' : p[i]['tzone'],
        'organisatorDisplayName' : p[i]['merc'],
        'location': p[i]['loc'],
        'publishSearchEngines' : False,
        'format': 'JSON',
        'version': 1
    }

    xingeventsresponse = requests.post(XING_URL, params=xingeventsparams)
    print(xingeventsresponse.text) #TEXT/HTML
    status = xingeventsresponse.status_code
    print(status)
    if(status == 201):
        yes = 1
        cur.execute("UPDATE product SET s = ? WHERE rowid=?",(yes, p[i]['rowid']))
        print("mark done for row:",p[i]['rowid'])

    pattributes = {'data':{'attributes':{
            'description': p[i]['des'],
            'end_date': p[i]['edate'],
            'end_time': p[i]['etime'],
            'promoter_name': p[i]['merc'],
            'public': False,
            'start_date': p[i]['sdate'],
            'start_time': p[i]['stime'],
            'time_zone': p[i]['tzone'],
            'title': p[i]['name'],
            'venue_name': p[i]['loc']
            }
            }}

    picaticdata = json.dumps(pattributes)

    picaticresponse = requests.post(PICATIC_URL, data=picaticdata, headers = {
        "Authorization": "Bearer "+picatickey
    })
    print(picaticresponse.text) #TEXT/HTML
    status = picaticresponse.status_code
    print(status)
    print(picaticresponse.reason)
    if(status == 201):
        yes = 1
        cur.execute("UPDATE product SET s = ? WHERE rowid=?",(yes, p[i]['rowid']))
        print("mark done for row:",p[i]['rowid'])


conn.commit()
cur.close()
