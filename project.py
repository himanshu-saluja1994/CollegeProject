from linkedin import linkedin
from credentials import *
# Define CONSUMER_KEY, CONSUMER_SECRET,  
# USER_TOKEN, and USER_SECRET from the credentials 
# provided in your LinkedIn application

#CONSUMER_KEY = '7554sf7bkebvrr'
#CONSUMER_SECRET = '18TLlhnvN7ooKEDP'
#USER_TOKEN = '53cab7c3-f3c5-4037-92f0-2ad8a5cc3c34'
#USER_SECRET = 'b4b71173-0fe5-4c1e-bbd4-a9fdcd98aa37'

#RETURN_URL = '' # Not required for developer authentication

# Instantiate the developer authentication class

auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
		                                USER_TOKEN, USER_SECRET, 
						                                RETURN_URL, 
										                                permissions=linkedin.PERMISSIONS.enums.values())

# Pass it in to the app...

app = linkedin.LinkedInApplication(auth)

# Use the app...

app.get_profile()

import json

connections = app.get_connections()

connections_data = 'linkedin_connections.json'

f = open(connections_data,'w')
f.write(json.dumps(connections,indent=1))
f.close()

my_positions = app.get_profile(selectors=['positions'])
print json.dumps(my_positions, indent=1)

connection_id = connections['values'][0]['id']
connection_positions = app.get_profile(member_id=connection_id, 
		                                       selectors=['positions'])
print json.dumps(connection_positions, indent=1)
