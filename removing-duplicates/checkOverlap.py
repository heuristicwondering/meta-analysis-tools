# Checking the amount of overlap between a subset and superset of scraped results.
# This is used to verify if I really need to run more refined searches or just the
# broader searches
import csv

def list2dict(dlist):
    try:
        keys = dlist[0].keys()
    except:
        keys = []
    ldict = {key: list() for key in keys}

    for d in dlist:
        for k in keys:
            ldict[k].append(d[k])

    return ldict


def checkOverlap(superset_file, subset_file):
    superset_reader = csv.DictReader(open(superset_file))
    subset_reader = csv.DictReader(open(subset_file))

    superset_data = []
    subset_data = []

    for line in superset_reader:
        superset_data.append(line)

    for line in subset_reader:
        subset_data.append(line)

    superset_data = list2dict(superset_data)
    subset_data = list2dict(subset_data)

    if len(superset_data) > 0 and len(subset_data) > 0:
        overlap = set(subset_data['titles']).intersection(set(superset_data['titles']))
        return len(overlap)/len(subset_data['titles'])
    else:
        return 0