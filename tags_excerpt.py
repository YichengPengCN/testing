import requests
import csv
import pymongo
from pymongo import MongoClient, InsertOne
import pandas as pd

# set up local db, just for testing, need to refine for backend
client = pymongo.MongoClient()
db = client["FIT3170"]
collection = db["Testing"]

# df = pd.read_csv("tagWithExcerpt.csv")
# data = df.to_dict(orient="records")
# collection.insert_many(data)
# collection.update_many({},{"$set":{"synonyms":[]}})
#
#
# with open ("tagSynonym.csv",'r') as ts:
#     reader = csv.reader(ts,delimiter="\t")
#     for i, line in enumerate(reader):
#         tagName = line[0].rpartition(',')[0]
#         tagSynonym = line [0].partition(',')[2].replace('"','')
#         print(tagName,tagSynonym)
#         if collection.find({}, {"tagName":tagName}):
#             collection.update_one({"tagName": tagName}, {"$push": {"synonyms": tagSynonym}})
#
#
# collection.update_many({},{"$set":{"topTenQuestion":[]}})




with open("tag_topQuestion1.csv", "a") as tt:
    writer = csv.writer(tt)
    writer.writerow(['tagName', 'questionTitle', 'questionLink'])
    for tag in collection.find({},{"tagName":"assembly"}):
        tagName = tag.get('tagName')

        print(f'------ {tagName}  is in processing ------')
        r = requests.get(
            f'https://api.stackexchange.com/2.3/tags/{tagName}/faq?site=stackoverflow&filter=!)R8hiMG-Yk6sUIhoN)QaR1TI&key=yz7n)sw4iQVUi0vE4h33AQ((')
        result = r.json()['items']
        resultLen = len(result)
        if resultLen == 0:
            continue
        elif 6 >= resultLen > 0:
            for i in range(resultLen):
                writer.writerow([tag.get('tagName'), result[i].get('title'), result[i].get('link')])
        else:
            for i in range(6):
                writer.writerow([tag.get('tagName'), result[i].get('title'), result[i].get('link')])

        print(f'----tag {tag.get("tagName")} is done----')
