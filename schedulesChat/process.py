from striprtf.striprtf import rtf_to_text
import json, requests, urllib
from types import SimpleNamespace
import datetime, uuid

user_url = "https://schedules-chat-default-rtdb.firebaseio.com/users.json"

def javaTime(d:datetime):
    return d.strftime("%Y-%m-%dT%H:%M:%S.%f")

def parseEvent(x, date_str):
    brief = datetime.datetime.strptime((date_str+":"+x["brf"]), '%d-%b-%Y:%H%M')
    takeoff = datetime.datetime.strptime((date_str+":"+x["lnch"]), '%d-%b-%Y:%H%M')
    land = datetime.datetime.strptime((date_str+":"+x["Land"]), '%d-%b-%Y:%H%M')
    instructor = Person(x["instructor"], "")
    students = []
    if x["student1"] != "":
        students.append(Person(x["student1"], x["code1"]))
    if x["STUDENT2"] != "":
        students.append(Person(x["STUDENT2"], x["CODE2"]))
    return Event(brief, takeoff, land, instructor, students)

def getID(per):
    query = {
        'orderBy': '"Name"',
        'equalTo': per.name,
        'print': 'pretty'
            }
    #print(urllib.parse.urlencode(query, quote_via=quote
    user = user_url + '?orderBy="name"&equalTo="' + urllib.parse.quote(per.name) + '"&print=pretty'
    r = requests.get(user)

    if r.json() == {}:
        return("0000000000")
    else:
        return(next(iter(r.json())))

class Person(dict):
    name = ""
    code = ""

    def __init__(self, name, code):
        dict.__init__(self, name=name, code=code)
        self.name = name
        self.code = code


class Event(dict):
    brief = datetime.datetime.now()
    takeoff = datetime.datetime.now()
    land = datetime.datetime.now()
    instructor = Person("", "")
    students = []

    def __init__(self, brief, takeoff, land, instructor, students):
        dict.__init__(self, brief=javaTime(brief), takeoff=javaTime(takeoff), land=javaTime(land), instructor=instructor, students=students)
        self.brief = brief
        self.takeoff = takeoff
        self.land = land
        self.instructor = instructor
        self.students = students

class Schedule(dict):
    date = datetime.datetime.now()
    notes = ""
    flights = []
    sims = []

    def __init__(self, date, notes, flights, sims):
        dict.__init__(self, date=javaTime(date), notes=notes, flights=flights, sims=sims)
        self.date = date
        self.notes = notes
        self.flights = flights
        self.sims = sims


rtf = open("sch_json.rtf").read()
text = rtf_to_text(rtf)
text = text.replace("“", "\"")
text = text.replace("”", "\"")
data = json.loads(text)


#print(data)

flights = []
sims = []
for flight in data["flights"]:
    if flight == {}:
        break
    else:
        flights.append(parseEvent(flight, data["date"]))
for sim in data["SIMS"]:
    if sim == {}:
        break
    else:
        sims.append(parseEvent(sim, data["date"]))

#    print("%s/%s/%s:\t\t%s\n%s:%s\t%s:%s\n" % (flight["brf"], flight["lnch"], flight["Land"], flight["instructor"], flight["student1"], flight["code1"], flight["STUDENT2"], flight["CODE2"]))
schedule = Schedule(datetime.datetime.strptime(data["date"], '%d-%b-%Y'), data["flight_notes"], flights, sims)

print("Schedule for %s:" % schedule.date.strftime("%d %b %Y"))

#for flight in schedule.flights:
#    print(flight.instructor.name)

print(json.dumps(schedule, indent=2))

print(getID(schedule.flights[0].instructor))
print(getID(schedule.flights[1].instructor))
