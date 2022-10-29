import webbrowser
import requests
from bs4 import BeautifulSoup
from soupsieve import select_one


## get the webpage
r = requests.get('https://docenti.unimc.it/s.pierosara/timetable/26244')

## get the html into soup
soup = BeautifulSoup(r.content, 'html.parser')

timetable = soup.find(id = "timetable")
lections = timetable.find_all("li")

for lection in lections:
    date = lection.find(class_ = "date")
    day = lection.find(class_ = "day-number").text.strip()
    month = lection.find(class_ = "month").text.strip()

    time = lection.find(class_ = "time").text
    place = lection.find(class_ = "place").text
    print(day, month, time, place)


##print (soup.prettify())



##print(r.content[:100])