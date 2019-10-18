from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os
from azure.cosmos import cosmos_client
import json
import urllib3




app = Flask(__name__)


CONFIG = {
    "ENDPOINT": "https://localhost:8081",
    "PRIMARYKEY": "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
    "DATABASE": "CosmosDatabase",  # Prolly looks more like a name to you
    "CONTAINER": "CosmosContainer"  # Prolly looks more like a name to you
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONTAINER_LINK = f"dbs/{CONFIG['DATABASE']}/colls/{CONFIG['CONTAINER']}"
FEEDOPTIONS = {}
FEEDOPTIONS["enableCrossPartitionQuery"] = True
# There is also a partitionKey Feed Option, but I was unable to figure out how to us it.

QUERY = {
    "query": f"SELECT * from c"
}

ctr = {
    "query": f"SELECT VALUE COUNT(1) FROM myCollection"
}

# Initialize the Cosmos client
client = cosmos_client.CosmosClient(
    url_connection=CONFIG["ENDPOINT"], auth={"masterKey": CONFIG["PRIMARYKEY"]}
)

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
def index():
    results = client.QueryItems(CONTAINER_LINK, QUERY, FEEDOPTIONS)
    counter = client.QueryItems(CONTAINER_LINK, ctr, FEEDOPTIONS)
    counter = (list(counter)[0])
    mylist = []
    
    # for item in results:
    #     for i in list(item):
    #         if(type(item[i]) is dict):
    #             # print("Yes")
    #             for k, v in item[i].items():
    #                 #print(k, ":", v)
    #                 mylist.append([k, v])
    #         else: 
    #             #print(i, ":" , item[i])
    #             mylist.append([i, item[i]])
    #for item in results: 
    #    for key in item:
    #        if(type(item[key]) is not dict):
                #print(key, item[key])
    #        else: 
                #print(key)
                #for k, v in item[key].items():
    #                print(k, v)
    return render_template("index.html", results=results, mylist=mylist, counter=counter)


@app.route("/update")
def update ():
    id=request.values.get("_id")
    key=request.args.get('key')
    item=request.args.get('item')
    #print(key)
    #print(item)
    select_query = {
    "query": f"SELECT * from c where c.id=\"{id}\""  
    }   
    results = client.QueryItems(CONTAINER_LINK, select_query, FEEDOPTIONS)
    for x in results: 
        x["summary"] = "bc"
    return render_template('update.html', id=id, results=results, key=key, item=item)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	#name=request.form.get("message")
    # client.UpsertItem(CONTAINER_LINK, name)
    #name = request.form.get("message")
    results = client.QueryItems(CONTAINER_LINK, QUERY, FEEDOPTIONS)
    key = request.form.get("key")
    item = request.form.get("item")
    id=request.form.get("id")
    sid = request.form.get("sid")

    if sid is None:
        for i in results:
            if i["id"] == id:
                i[key] = item
                client.UpsertItem(CONTAINER_LINK, i)

    else:
        for i in results:
            if i["id"] == id:
                i[sid][key] = item
                client.UpsertItem(CONTAINER_LINK, i)
    return redirect("/")
