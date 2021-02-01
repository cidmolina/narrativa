from datetime import date, datetime, timedelta
import json
import pandas as pd
import os 

## Time functions
def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

## Initialization:
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
header_added = False

# Import Json and export CSV with relevant data:
for i in os.listdir('data'): # Loop every file (1 file per week)
    
    datefile = i.split('.')[0] # File loaded, corresponding to a week
    weekinit = datetime.strptime(datefile, "%Y-%m-%d").date() # Initial date of that week

    #print(i)

    with open(THIS_FOLDER+'/data/' + datefile + '.json') as data_file:    
        d = json.load(data_file)  

    for j in range(0,7): # Loop every day 

        day = (weekinit + timedelta(days=j)).strftime("%Y-%m-%d")
        #print(day)
        
        df = pd.DataFrame(d["dates"][day]["countries"]["Spain"]["regions"]) # Select relevant key
        #print(df)

        df.drop(['links','sub_regions'], axis=1, inplace=True) # Remove nested fields corresponding to subregions

        # Final output file should have 15 (weeks) * 7 (days) * 17 (regions) + header = 1996 lines

        if not header_added: # Add column names in the first iteration of the loop
            df.to_csv('output.csv', mode='a', header=True, index=False)
            header_added = True
        else:
            df.to_csv('output.csv', mode='a', header=False, index=False) 

