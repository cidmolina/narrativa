from datetime import date, datetime, timedelta
import requests
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

## Functions:

# Iterate over a period of time every delta
def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

# GET request to COVID API and write output as json file
def weeklycovid(startweek, finalweek, filename):
    r = requests.get('https://api.covid19tracking.narrativa.com/api/country/spain?date_from={}&date_to={}'.format(startweek, finalweek))
    coviddata = r.json()
    with open(THIS_FOLDER + "/" + filename, 'w') as outfile:
        json.dump(coviddata,  outfile)

## Initialization variables
initial_date = date(2020, 3, 20)
final_date = date(2020, 6, 30)
weeks = []

## Code:
#Generate a list with starting date of every week:
for day in datespan(initial_date, final_date, 
                     delta=timedelta(days=7)):
     weeks.append(day)

# GET request to the API and write to a json file for every week:
for i in weeks:
    s = i.strftime("%Y-%m-%d")
    t = (i+timedelta(days=7)).strftime("%Y-%m-%d")
    f = s + '.json'
    weeklycovid(s, t, f) 
#replace("/","_")
