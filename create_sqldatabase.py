import mysql.connector
import pandas as pd
import os
from itertools import islice
import csv

##### CREATE NARRATIVA_COVID DATABASE

#mydb = mysql.connector.connect(
#  host="localhost",
#  user="root",
#  password="brontosaurio1"
#)

#mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE narrativa_covid")
#mycursor.execute("SHOW DATABASES")

#for x in mycursor:
#  print(x) 

#mydb.commit()
#mycursor.close()

#####


# Import CSV
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
df_covid = pd.read_csv(THIS_FOLDER + "/" + "covid_data.csv", sep =",")
df_meta = pd.read_csv(THIS_FOLDER + "/" + "metadata.csv", sep =";")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="brontosaurio1",
  database="narrativa_covid"
)

mycursor = mydb.cursor()

# Create Table
sql = "DROP TABLE metadata"
mycursor.execute(sql) 
mycursor.execute('CREATE TABLE narrativa_covid.metadata (Population INT, Region VARCHAR(100), Age65 DOUBLE, Income DOUBLE, id VARCHAR(100) NOT NULL)')

# Insert DataFrame to Table
for index,row in df_meta.iterrows():
  sql="INSERT INTO narrativa_covid.metadata VALUES (%s,%s,%s,%s,%s)"
  mycursor.execute(sql, tuple(row.values))

mydb.commit()

sql = "DROP TABLE covid_data"
mycursor.execute(sql) 
mycursor.execute('CREATE TABLE covid_data (date DATE, id VARCHAR(50), name VARCHAR(50), \
source VARCHAR(50), today_confirmed INT, today_deaths INT, today_hospitalised_patients_with_symptoms INT, \
today_intensive_care INT, today_new_confirmed INT, today_new_deaths INT, today_new_hospitalised_patients_with_symptoms INT, \
today_new_intensive_care DOUBLE, today_new_open_cases DOUBLE, today_new_recovered DOUBLE, today_new_total_hospitalised_patients DOUBLE, \
today_open_cases DOUBLE, today_recovered DOUBLE, today_total_hospitalised_patients DOUBLE, today_vs_yesterday_confirmed DOUBLE, \
today_vs_yesterday_deaths DOUBLE, today_vs_yesterday_hospitalised_patients_with_symptoms DOUBLE, today_vs_yesterday_intensive_care DOUBLE, \
today_vs_yesterday_open_cases DOUBLE, today_vs_yesterday_recovered DOUBLE, today_vs_yesterday_total_hospitalised_patients DOUBLE, \
yesterday_confirmed DOUBLE, yesterday_deaths DOUBLE, yesterday_hospitalised_patients_with_symptoms DOUBLE, yesterday_intensive_care DOUBLE, \
yesterday_open_cases DOUBLE, yesterday_recovered DOUBLE, yesterday_total_hospitalised_patients DOUBLE)')

df_covid.fillna(0)
for index,row in df_covid.iterrows():
  sql="INSERT INTO narrativa_covid.covid_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
  mycursor.execute(sql, tuple(row.values))
