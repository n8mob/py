import json
import csv

def csvify(json_file_name, csv_file_name):
    with open(json_file_name) as jsonfile:
        with open(csv_file_name, 'w+') as csvfile:
            cwriter = csv.writer(csvfile)
            keys = jsonfile[0].keys()
            cwriter.writerow(keys)
            for jrow in jsonfile:
                cwriter.writerow(jrow[key] for key in keys)
    
