import os
import csv
import random
import json
import operator
from nltk.metrics.distance import jaccard_distance
from cluster import HierarchicalClustering

CSV_FILE = os.path.join('connections.csv')

OUT_FILE = 'viz/d3-data.json'


DISTANCE_THRESHOLD = 0.5
DISTANCE = jaccard_distance


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

    all_titles = list(set(all_titles))
    
    # Define a scoring function
    def score(title1, title2): 
        return DISTANCE(set(title1.split()), set(title2.split()))

    # Feed the class your data and the scoring function
    hc = HierarchicalClustering(all_titles, score)

    # Cluster the data according to a distance threshold
    clusters = hc.getlevel(DISTANCE_THRESHOLD)

    # Remove singleton clusters
    clusters = [c for c in clusters if len(c) > 1]
  # print clusters
    # Round up contacts who are in these clusters and group them together

    clustered_contacts = {}
    for cluster in clusters:
        clustered_contacts[tuple(cluster)] = []
        for contact in contacts:
            for title in contact['Job Titles']:
                if title in cluster:
                    clustered_contacts[tuple(cluster)].append('%s %s %s'
                            % (contact['First Name'], contact['Last Name'] ,contact['Job Title']))

    return clustered_contacts

def display_output(clustered_contacts):
    
    for titles in clustered_contacts:
        common_titles_heading = 'Common Titles: ' + ', '.join(titles)
       # print common_titles_heading
	print '\n'
	print titles
	ll=[]
	d=dict()
	for term_sep in titles:
	 #   print term_sep
	    sp_sep_ti=term_sep.split()
	#    print sp_sep_ti
	    for sl in sp_sep_ti:
		if sl in d:
		    d[sl]=d[sl]+1
		else:
		    d[sl]=1;
		ll.append(sl)
	print d
	#print max(d, key=d.get)
        #descriptive_terms = set(titles[0].split())
        #for title in titles:
        #    descriptive_terms.intersection_update(set(title.split()))
       # descriptive_terms_heading = 'Descriptive Terms: ' \
       #    + ', '.join(descriptive_terms)
       # print descriptive_terms_heading
        #print '-' * max(len(descriptive_terms_heading), len(common_titles_heading))
       #print '\n'.join(clustered_contacts[titles])
        #print

def write_d3_json_output(clustered_contacts):
    
    json_output = {'name' : 'My LinkedIn', 'children' : []}

    for titles in clustered_contacts:

        descriptive_terms = set(titles[0].split())
        for title in titles:
            descriptive_terms.intersection_update(set(title.split()))

        json_output['children'].append({'name' : ', '.join(descriptive_terms)[:30], 
                                    'children' : [ {'name' : c.decode('utf-8', 'replace')} for c in clustered_contacts[titles] ] } )
    
        f = open(OUT_FILE, 'w')
        f.write(json.dumps(json_output, indent=1))
        f.close()
    
clustered_contacts = cluster_contacts_by_title(CSV_FILE)
display_output(clustered_contacts)
#write_d3_json_output(clustered_contacts)
