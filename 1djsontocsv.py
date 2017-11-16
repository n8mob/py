import json
import csv

"""
Converts a simple JSON array to a CSV file
Assumes that all the JSON objects in the array have the same structure
"""

def csvify(json_file_name, csv_file_name):
    with open(json_file_name) as jsonfile:
        with open(csv_file_name, 'w+') as csvfile:
            cwriter = csv.writer(csvfile)
            keys = jsonfile[0].keys()
            cwriter.writerow(keys)
            for jrow in jsonfile:
                cwriter.writerow(jrow[key] for key in keys)
    
