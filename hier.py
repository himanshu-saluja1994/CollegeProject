import os
import csv
import random
import json
import operator
from nltk.metrics.distance import edit_distance
from cluster import HierarchicalClustering

CSV_FILE = os.path.join('connections.csv')

OUT_FILE = 'viz/d3-data.json'


DISTANCE_THRESHOLD = 0
DISTANCE = edit_distance


SAMPLE_SIZE = 500

def cluster_contacts_by_title(csv_file):

    transforms = [
        ('Sr.', 'Senior'),
        ('Sr', 'Senior'),
        ('Jr.', 'Junior'),
        ('Jr', 'Junior'),
        ('CEO', 'Chief Executive Officer'),
        ('COO', 'Chief Operating Officer'),
        ('CTO', 'Chief Technology Officer'),
        ('CFO', 'Chief Finance Officer'),
        ('VP', 'Vice President'),
        ]

    separators = ['/', 'and', '&']

    csvReader = csv.DictReader(open(csv_file), delimiter=',', quotechar='"')
    contacts = [row for row in csvReader]

    all_titles = []
    for i, _ in enumerate(contacts):
        if contacts[i]['Job Title'] == '':
            contacts[i]['Job Titles'] = ['']
            continue
        titles = [contacts[i]['Job Title']]
        for title in titles:
            for separator in separators:
                if title.find(separator) >= 0:
                    titles.remove(title)
                    titles.extend([title.strip() for title in title.split(separator)
                                  if title.strip() != ''])

        for transform in transforms:
            titles = [title.replace(*transform) for title in titles]
        contacts[i]['Job Titles'] = titles
        all_titles.extend(titles)

    
    print all_titles
    print len(all_titles)
    unique_title=[]
    d=dict()
    for titles in all_titles:
	if titles in d:
	    d[titles]=d[titles]+1
	else:
	    d[titles]=1
	    unique_title.append(titles);
    #print unique_title
    for r in unique_title:
	print r
    print len(unique_title)


clustered_contacts = cluster_contacts_by_title(CSV_FILE)

