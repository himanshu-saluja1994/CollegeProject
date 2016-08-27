import re
from project import *
from geopy import geocoders
GEO_APP_KEY = 'AjBl_exEOrwQdY8PVGenQj89LFdjxKn2ciZKAwX-Gfn2rbESjpcwnaQyokPAwOGU'
g = geocoders.Bing(GEO_APP_KEY)

pattern = re.compile('.*([A-Z]{2}).*')
    
def parseStateFromBingResult(r):
    result = pattern.search(r[0][0])
    if result == None: 
        print "Unresolved match:", r
        return "???"
    elif len(result.groups()) == 1:
        print result.groups()
        return result.groups()[0]
    else:
        print "Unresolved match:", result.groups()
        return "???"

    
transforms = [('Greater ', ''), (' Area', '')]

results = {}
for c in connections['values']:
    if not c.has_key('location'): continue
    if not c['location']['country']['code'] == 'us': continue
        
    transformed_location = c['location']['name']
    for transform in transforms:
        transformed_location = transformed_location.replace(*transform)
    
    geo = g.geocode(transformed_location, exactly_one=False)
    if geo == []: continue
    parsed_state = parseStateFromBingResult(geo)
    if parsed_state != "???":
        results.update({c['location']['name'] : parsed_state})
    
print json.dumps(results, indent=1)
