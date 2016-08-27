import os
import csv
from collections import Counter
from operator import itemgetter
from prettytable import PrettyTable

CSV_FILE = os.path.join('con1.csv')
transforms = [(', Inc.', ''), (', Inc', ''), (', LLC', ''), (', LLP', ''),
               (' LLC', ''), (' Inc.', ''), (' Inc', ''),('Indian Institute of Information Technology, Allahabad, India','Indian Institute of Information Technology, Allahabad, India '),('IIIT-A','Indian Institute of Information Technology, Allahabad, India '),('IIIT Allahabad','Indian Institute of Information Technology, Allahabad, India '),('iiit allahabad','Indian Institute of Information Technology, Allahabad, India '),('IIIT A','Indian Institute of Information Technology, Allahabad, India '),('IIITA','Indian Institute of Information Technology, Allahabad, India ')]

csvReader = csv.DictReader(open(CSV_FILE), delimiter=',', quotechar='"')
contacts = [row for row in csvReader]
#print contacts
companies = [d['Company'].strip() for d in contacts if d['Company'].strip() != '']

for i, _ in enumerate(companies):
	for transform in transforms:
		companies[i] = companies[i].replace(*transform)
	
#print companies
pt = PrettyTable(field_names=['Company', 'Freq'])
pt.align = 'l'
c = Counter(companies)

#print c['Practo']

[pt.add_row([company, freq]) 
 for (company, freq) in sorted(c.items(), key=itemgetter(1), reverse=True) 
     if freq >= 1]
print pt
