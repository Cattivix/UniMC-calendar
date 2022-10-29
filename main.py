import webbrowser
import requests
from bs4 import BeautifulSoup
from soupsieve import select_one


## get the webpage
r = requests.get('https://docenti.unimc.it/s.pierosara/timetable/26244')

## get the html into soup
soup = BeautifulSoup(r.content, 'html.parser')

timetable = soup.find(id = "timetable")
time = timetable.ul.li
print(time[0])


##print (soup.prettify())



##print(r.content[:100])