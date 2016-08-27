import os
from operator import itemgetter
import csv
from prettytable import PrettyTable
from collections import Counter



CSV_FILE = os.path.join('con1.csv')

transforms = [
    ('Sr.', 'Senior'),
    ('CFO', 'Chief Finance Officer'),
    ('Sr', 'Senior'),
    ('VP', 'Vice President'),
    ('Jr.', 'Junior'),
    ('CTO', 'Chief Technology Officer'),
    ('Jr', 'Junior'),
    ('CEO', 'Chief Executive Officer'),
    ('COO', 'Chief Operating Officer'),
    
    
    
    ]

csvReader = csv.DictReader(open(CSV_FILE), delimiter=',', quotechar='"')
conta = [row for row in csvReader]



til = []
for cont in conta:
    til.extend([d.strip() for d in cont['Job Title'].split('/')
                  if cont['Job Title'].strip() != ''])


tokens = []
for title in til:
    tokens.extend([t.strip(',') for t in title.split()])
pt2 = PrettyTable(field_names=['Tokens', 'Frequency'])
pt2.align = 'l'
c = Counter(tokens)
[pt2.add_row([tokens, frequency]) 
 for (tokens, frequency) in sorted(c.items(), key=itemgetter(1), reverse=True) 
     if frequency > 1 and len(tokens) > 2]
print ""

print pt2

print til
for i, _ in enumerate(til):
    for transform in transforms:
        til[i] = til[i].replace(*transform)



pti = PrettyTable(field_names=['Titles', 'Frequency'])
pti.align = 'l'
c = Counter(til)
[pti.add_row([titles, frequency]) 
 for (titles, frequency) in sorted(c.items(), key=itemgetter(1), reverse=True) 
     if frequency > 1]
print ""
print pti



