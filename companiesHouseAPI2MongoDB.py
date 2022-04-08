#!/usr/bin/env python

import json
import csv
import sys
import requests
import pymongo
import sys

from requests.auth import HTTPBasicAuth

print("Companys House Search Tool")

client = pymongo.MongoClient("localhost", 27017)
db = client.companyhouse

#define API key
APIKEY = "ADD YOUR KEY HERE"

#define arguments
q = sys.argv[1]

search = "https://api.companieshouse.gov.uk/search/companies?q="+q+"&items_per_page="+"100"
r = requests.get(search, auth=HTTPBasicAuth(APIKEY, ""))

jData = json.loads(r.content)

for data in jData["items"]:
  officers = "https://api.companieshouse.gov.uk/company/"+data["company_number"]+"/officers"
  histories = "https://api.companieshouse.gov.uk/company/"+data["company_number"]+"/filing-history"

  x = requests.get(histories, auth=HTTPBasicAuth(APIKEY, ""))
  r = requests.get(officers, auth=HTTPBasicAuth(APIKEY, ""))

  histories = json.loads(x.content)
  officer = json.loads(r.content)

  company_name = data["title"]
  company_number = data["company_number"]
  company_status = data["company_status"]
  date_of_creation = data["date_of_creation"]
  address_snippet = data["address_snippet"]

  try:
    for history in histories["items"]:
      description_values = history["description_values"]

  except:
    print("")
  
  try:
    for officer in officer["items"]:
      officer_name = officer["name"]
      officer_title = officer["officer_title"]

  except:
    print("")

  try:
    db.companyhouse.insert_one({
      "name": title,
      "company_number": company_number, 
      "company_status": company_status,
      "date_of_creation": date_of_creation,
      #"officer_name": officer_name,
      #"officer_title:" officer_title,
      "history": description_values})
  
  except:
    print("error")

  print("DONE")
  
    
    
