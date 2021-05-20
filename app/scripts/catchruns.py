import os
import json
import csv

csvfile = open("../runs/runs.csv", 'w', newline='')
writer = csv.writer(csvfile)
objetivo = 'First Training'

for root, directories, files in os.walk("../runs", topdown=True):
    for dic in directories:
        if dic.lower() != "models":
            file = "../runs/"+dic+"/Parameters.json"
            with open(file, "r") as json_file:
                params = json.load(json_file)

                row = [objetivo,
                       int(params.get("duration", 0)),
                       params.get("initial balance", ''),
                       params.get("training episodes", ''),
                       params.get("training batch size", ''),
                       params.get("lookback window size", ''),
                       params.get("lr", ''),
                       params.get("epochs", ''),
                       params.get("batch size", ''),
                       params.get("model", ''),
                       params.get("Actor name", '').split('_')[0],
                       params.get("Actor Nodes", ''),
                       params.get("Critic Nodes", ''),
                       params.get("Indicators", '')]

                writer.writerow(row)
