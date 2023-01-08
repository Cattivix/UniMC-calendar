import datetime
import requests
from bs4 import BeautifulSoup
from soupsieve import select_one
from collections import defaultdict
import colorama
from time import sleep
import os

# initialize colorama
colorama.init()

# create a dictionary to store the lections by date
calendar = defaultdict(list)

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
i = 0


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

print("Inizio recupero orari...")

## iterate through the links and do stuff
for link in links:
    ##clear the lections list
    lections = []   
    ## get the webpage
    try: 
        r = requests.get(link)

    except requests.exceptions.RequestException as e:
    # handle exceptions here
        print(e)
        exit()

    else:
        ## get the html into soup, get the timetable of the lections
        soup = BeautifulSoup(r.content, 'html.parser')
        timetable = soup.find(id = "timetable")
        if timetable is None:
            print(link, "Questo corso non ha orari. Hai selezionato l'anno giusto?")
            print("Riprovo...")
            sleep(0.3)

            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html.parser')
            timetable = soup.find(id = "timetable")
            if timetable is None:
                print(link, "Continuo a non trovare orari per questo corso. Ricontrolla il link e riprova")
                exit()



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
            ## if lections arent expired, append them to the calendar
            if ((today.month == month) and (today.day <= day)) or (today.month < month):
                calendar[(day, month)].append((start, end, title, place))
        i+= 1
        if i == 1:
            os.system('cls')
            print(f"{i} corso fatto...")
        else:
            os.system('cls')
            print(f"{i} corsi fatti...")
        sleep(0.2)

## if no lections are scraped, exit the program
if not calendar:
    print("I corsi selezionati non hanno piu' lezioni.")
    exit()

## clear the console
os.system('cls')


## used to check if the schedule is for the current week or for the next one
skipweek = False

## dictionary for weekdays
weekdays_dic = {0 : 'lunedì', 1 : 'martedì', 2 : 'mercoledì', 3 : 'giovedì', 4 : 'venerdì', 5 : 'sabato', 6 : 'domenica'}


## if today is saturday or sunday, warn the user and show lectures for next week
print()
if today.weekday() >= 5:
    if today.weekday() == 5:
     today += datetime.timedelta(days = 2)  
    if today.weekday() == 6:
     today += datetime.timedelta(days = 1)
print("Le lezioni di questa settimana sono finite, ecco le lezioni della prossima settimana. \n ")
skipweek = True

## calculate the start and end dates of the week for the target date
start_week = today - datetime.timedelta(today.weekday())
end_week = start_week + datetime.timedelta(days = 6)



# create a list of tuples containing the date and lectures for each date in the target week
week_lectures = [(datetime.date.fromordinal(date), sorted(calendar[(datetime.date.fromordinal(date).day, datetime.date.fromordinal(date).month)], key=lambda x: (x[0], x[1]))) for date in range(start_week.toordinal(), end_week.toordinal()+1) if (datetime.date.fromordinal(date).day, datetime.date.fromordinal(date).month) in calendar]

## if there are no lections found in the current week, exit the program
if not week_lectures:
    print("Non ci sono lezioni questa settimana. \n")

## print the sorted lectures to the console
for date, lectures in week_lectures:
    day, month, = date.day, date.month
    if day == today.day and month == today.month and skipweek is False:
        print(colorama.Fore.LIGHTRED_EX + f"Lezioni di oggi:")
    else:
        currentday = datetime.date(today.year, month, day)

        print(colorama.Fore.LIGHTRED_EX + f"Lezioni di {weekdays_dic[currentday.weekday()]} {day}/{month}:")

    # reset the color to the default
    print(colorama.Style.RESET_ALL)

    for lecture in lectures:
        start, end, title, place = lecture
        print(f"  {start} - {end}, {title}, {place}")
    print("\n")