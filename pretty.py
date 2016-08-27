from prettytable import PrettyTable
import json
from project import *

connections = json.loads(open('linkedin_connections.json').read())
pt = PrettyTable(field_names=['Name', 'Location'])
pt.align = 'l'

[ pt.add_row((c['firstName'] + ' ' + c['lastName'], c['location']['name'])) 
  for c in connections['values']
        if c.has_key('location')]

print pt

