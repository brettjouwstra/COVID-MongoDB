from dotenv import load_dotenv
from pymongo import MongoClient
import os
import bson
from datetime import datetime

# My Local Mongo Instance
loc_client = MongoClient('192.168.1.5', 27017)
loc_db = loc_client['covid19']
loc_collection = loc_db['penn_co_sd']
loc_collection2 = loc_db['fargo']
loc_stats = loc_db.command('dbstats')

# Load config from a .env file:
load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

# Connect to your MongoDB cluster:
client = MongoClient(MONGODB_URI)
db = client['covid19']
collection = db['us_only']
collection_2 = db['global_and_us']

def get_dbnames():
# List all the databases in the cluster:
   for db_info in client.list_database_names():
      print(db_info)

def fullname_srch():
   pennington = collection.find_one({'combined_name': 'Pennington, South Dakota, US'})
   return pennington

def uid_srch_all(uid):
   penn_cnty_code = collection.find({'uid': uid})

   list_uids = []
   for data in penn_cnty_code:
      list_uids.append(data)
   
   return list_uids

# penn_co_uid = 84046103
# fargo = 84038017

# for item in uid_srch_all(fargo):
#    loc_collection2.insert_one(item)



def total_dead():
   sd = loc_collection.find({})
   nd = loc_collection2.find({})

   sd_dead = {}
   jun = 0
   july = 0
   aug = 0
   sept = 0
   october = 0

   for d in nd:
      first = d['date'].strftime('"%m/%d/%Y, %H:%M:%S"')[:3]
      second = first.replace('"', '')
      print(second)
      if second == str('06'):
         
         jun += int(d['deaths'])
   
      if second == str('07'):
         july += int(d['deaths'])

      if second == str('08'):
         aug += int(d['deaths'])

      if second == str('09'):
         sept += int(d['deaths'])
      
      if second == str('10'):
         october += int(d['deaths'])

   sd_dead['jun'] = jun
   sd_dead['july'] = july
   sd_dead['august'] = aug
   sd_dead['sept'] = sept
   sd_dead['october'] = october

   return sd_dead
      


# SD = {'jun': 273, 'july': 673, 'august': 993, 'sept': 1029, 'october': 948}
# ND = {'jun': 1844, 'july': 2229, 'august': 2356, 'sept': 2299, 'october': 1812}

def stats():
   call = loc_db.command("dbstats")
   database = call['db']
   datasize = call['dataSize'] / 1024
   objects = call['objects']
   collections = call['collections']

   return {'Database': str(database), 'Objects': str(objects), 'Collections': str(collections), 'Size': str(datasize)[:4] + 'Mb'}




