from pymongo import MongoClient
import os

mongoUri = 'mongodb://' + os.environ.get('DATABASE_USERNAME') + ':' + \
    os.environ.get('DATABASE_PASSWORD') + '@ds217360.mlab.com:17360/sightlines'
client = MongoClient(mongoUri)
db = client['sightlines']
result = db['alabamaStatisticalTerms']

matches = result.find({})
total = 0
for match in matches:
    count = match['count']
    if count > 0:
        total = total + count

print(total)
