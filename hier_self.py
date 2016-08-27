import os
import csv
import random
import json
import operator
from nltk.metrics.distance import edit_distance
from cluster import HierarchicalClustering

CSV_FILE = os.path.join('connections.csv')

OUT_FILE = 'viz/d3-data.json'


DISTANCE_THRESHOLD = 4
DISTANCE = edit_distance


SAMPLE_SIZE = 500

def cluster_contacts_by_title(csv_file):


    def score(title1, title2): 

        return DISTANCE((title1), (title2))
    all_titles=[]
    all_titles.append("Student")
    all_titles.append("Assistant Professor")
    all_titles.append("Student Ambassador")
    all_titles.append("Assistant Developer")
    all_titles.append("Human Resources")
    all_titles.append("Software Developer")
    all_titles.append("Head, Technical Affairs-Software")
    all_titles.append("Sofware Engineer")

    all_titles.append("Software Engineer")
    all_titles.append("Design Secretary")
    all_titles.append("Telesales Executive")
    all_titles.append("Filmmaker")
    all_titles.append("Writer")
    all_titles.append("Data Developer")
    all_titles.append("Software Developmer")
    all_titles.append("Co-founder")

    all_titles.append("Assistant Manager")
    
    all_titles.append("Management Trainee - Operations")
    all_titles.append("Oracle Database Administrator")
    all_titles.append("Key Account Manager")
    all_titles.append("Engineering Manager")
    all_titles.append("Talent Acquisition Manager")
    all_titles.append("Wireless Protocol Test Intern")

    all_titles.append("HR Executive")
    all_titles.append("IT Company")
    all_titles.append("Business Development Manager")
    all_titles.append("Member of Technical Staff")
    all_titles.append("Web Designer")
    all_titles.append("ECE Student")
    all_titles.append("Intern")
    all_titles.append("Head of Growth")

    all_titles.append("SA")
    all_titles.append("Manager (Technology)")
    all_titles.append("Systems Engineer")
    all_titles.append("Technical Team Member")
    all_titles.append("Business Developer")
    all_titles.append("system engineer")
    all_titles.append("Infrastructure Developer")
    all_titles.append("Engineer")
    all_titles.append("Mechanical Engineer")
    all_titles.append("Student Technical Assistant")
    all_titles.append("Senior Software Engineer")
    all_titles.append("Senior Software Developer")
    all_titles.append("Associate Professor")
    all_titles.append("Professor")
    all_titles.append("Software developer")
    all_titles.append("Director - Software Engineering")
    all_titles.append("Product Manager")






    hc = HierarchicalClustering(all_titles, score)

    # Cluster the data according to a distance threshold
    clusters = hc.getlevel(DISTANCE_THRESHOLD)
    print clusters

    score_matrix=[]
    min_d=1000000
    for title1 in all_titles:
	temp=[]
	for title2 in all_titles:
	    li1=title1.split(",")
	    li2=title2.split(",")
	    for ll1 in li1:
		min_d=100000
		for ll2 in li2:
		  #  print ll1,ll2
		    d=score(ll1,ll2)
		   # print d
		    min_d=min(min_d,d)
		#print "done"
	    
    	 #   print d
	    temp.append(min_d)
	score_matrix.append(temp);
  #  print score_matrix
    print len(all_titles)

     
    i=j=k=l=0
    mini=10000
    for l1 in score_matrix:
	j=0;
	for l2 in l1:
	    if l2 < mini and i!=j:
	        mini=l2
		k=i
		l=j
	    j=j+1
	i=i+1
#    print "%d %d",(k,l)
#    print mini
    clusters = [c for c in clusters if len(c) > 1]
  # print clusters
    # Round up contacts who are in these clusters and group them together
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
    clustered_contacts = {}
    for cluster in clusters:
        clustered_contacts[tuple(cluster)] = []
        for contact in contacts:
            for title in contact['Job Titles']:
                if title in cluster:
                    clustered_contacts[tuple(cluster)].append('%s %s '
                            % (contact['First Name'], contact['Last Name'] ))

    return clustered_contacts

   
def display_output(clustered_contacts):
    
    for titles in clustered_contacts:
        common_titles_heading = 'Common Titles: ' + ', '.join(titles)
       # print common_titles_heading
     #   print '\n'
      #  print titles
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
            #ll.append(sl)
    #    print d
        for key in d:
            #  print d[key]
            if (d[key] * 2) >= (len(d)):
                print key
	#print max(d, key=d.get)
        descriptive_terms = set(titles[0].split())
        for title in titles:
            descriptive_terms.intersection_update(set(title.split()))
        descriptive_terms_heading = 'Descriptive Terms: ' \
           + ', '.join(descriptive_terms)
        print descriptive_terms_heading
        print '-' * max(len(descriptive_terms_heading), len(common_titles_heading))
        print '\n'.join(clustered_contacts[titles])
        print

def write_d3_json_output(clustered_contacts):
    
    json_output = {'name' : 'My LinkedIn', 'children' : []}

    for titles in clustered_contacts:

        descriptive_terms = set(titles[0].split())
        #print descriptive_terms
        for title in titles:
            descriptive_terms.intersection_update(set(title.split()))
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
            #ll.append(sl)
        print d
        a=[]
        for key in d:
            #  print d[key]
            if (d[key] ) >= (len(titles)/2):
  #              print key
                a.append(key)
                
        print a
        print descriptive_terms

        json_output['children'].append({'name' : ', '.join(a), 
                                    'children' : [ {'name' : c.decode('utf-8', 'replace')} for c in clustered_contacts[titles] ] } )
    
        f = open(OUT_FILE, 'w')
        f.write(json.dumps(json_output, indent=1))
        f.close()
    
clustered_contacts = cluster_contacts_by_title(CSV_FILE)
display_output(clustered_contacts)
write_d3_json_output(clustered_contacts)

