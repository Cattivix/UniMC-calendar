import datetime
import requests
from bs4 import BeautifulSoup
from soupsieve import select_one




## class and list for lections, links list
class Lection:
    "lection class with lection data"
    def __init__(self, day, month, start, end, place):
        self.day = day
        self.month = month
        self.start = start
        self.end = end
        self.place = place

lections = []
links = []

## get date
today = datetime.date.today()

## dictionary for months manipulation
Months_dic = {'gen': 1, 'feb' : 2, 'mar' : 3, 'apr' : 4, 'mag' : 5, 'giu' : 6, 'lug' : 7, 'ago' : 8, 'set' : 9, 'ott' : 10, 'nov' : 11, 'dic' : 12}

## get links from text file, edit them to get the timetable URL
with open("links.txt" , "r") as openfileobj:

    for line in openfileobj:
        line.strip()
        lineobj = line.split('/')
        link = lineobj[0] + '//' + lineobj[2] + '/' + lineobj[3] + '/timetable/' + lineobj[6]
        links.append(link)


## iterate through the links and do stuff
for link in links:
    ##clear the lections list
    lections = []   
    ## get the webpage
    r = requests.get(link)
    print(link)

    ## get the html into soup, get the timetable of the lections
    soup = BeautifulSoup(r.content, 'html.parser')
    timetable = soup.find(id = "timetable")
    lections_raw = timetable.find_all("li")
    title = timetable.select('h1 > span')[1].get_text(strip=True)[13:] ## the splice removes academic year and blank spaces


    ## iterate through lections to scrape data
    for lection_raw in lections_raw:
        ## get and strip single elements of lection
        day = int(lection_raw.find(class_ = "day-number").text.strip())
        month = int(Months_dic.get(lection_raw.find(class_ = "month").text.strip()))
        time = lection_raw.find(class_ = "time").text.strip()
        place = lection_raw.find(class_ = "place").text.strip()

        ## split start and end hours
        start = time[ 0 : 5]
        end = time[-5:]

        ## if lections arent expired, append them to the list
        if ((today.month == month) and (today.day <= day)) or (today.month < month) or (today.year == 2022):
            lections.append( Lection(int(day), int(month), start, end, place))

    print(title)
    ##for obj in lections:
    ##    print(obj.day, obj.month, obj.start, obj.end, obj.place)
    print(len(lections))
   