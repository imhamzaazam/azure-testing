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
    for item in results: 
        for key in item:
            if(type(item[key]) is not dict):
                print(key, item[key])
            else: 
                print(key)
                for k, v in item[key].items():
                    print(k, v)
    return render_template("index.html", results=results, mylist=mylist, counter=counter)


@app.route("/update")
def update ():
    id=request.values.get("_id")
    select_query = {
    "query": f"SELECT * from c where c.id=\"{id}\""  
    }   
    results = client.QueryItems(CONTAINER_LINK, select_query, FEEDOPTIONS)
    
    return render_template('update.html', id=id, results=results)

@app.route("/action3", methods=['POST'])
def action3 ():
	name = request.form.get("message")
    #client.UpsertItem(CONTAINER_LINK, {"id": "pest"})
    s = name.replace("\'\"", "\"") 
    s = s.replace("\"\'", "\"")
    s = s.replace("\'", "\"")
    print(s)
    
    temp = json.loads(s) 
    #print(name)
    
    #json_acceptable_string = s.replace("'", """)
    #d = json.loads(json_acceptable_string)

    print(type(temp))
    #print(type(d))
    #d = json.loads(ini_string)
    #d = {"id" : "bcd"}
    
    client.UpsertItem(CONTAINER_LINK, temp)
    return redirect("/")
      

# @app.route("/action3", methods=['POST'])
# def action3 ():
# 	#Updating a Task with various references
# 	name=request.values.get("name")
# 	desc=request.values.get("desc")
# 	date=request.values.get("date")
# 	pr=request.values.get("pr")
# 	id=request.values.get("_id")
# 	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
# 	return redirect("/")
