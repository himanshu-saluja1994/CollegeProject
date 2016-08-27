import os
import json
from IPython.display import IFrame
from IPython.core.display import display
from geocode import *
# Load in a data structure mapping state names to codes.
# e.g. West Virginia is WV
codes = json.loads(open('states.json').read())

from collections import Counter
c = Counter([r[1] for r in results.items()])
states_freqs = { codes[k] : v for (k,v) in c.items() }

# Lace in all of the other states and provide a minimum value for each of them
states_freqs.update({v : 0.5 for v in codes.values() if v not in states_freqs.keys() })

# Write output to file
f = open('states-freqs.json', 'w')
f.write(json.dumps(states_freqs, indent=1))
f.close()

# IPython Notebook can serve files and display them into
# inline frames. Prepend the path with the 'files' prefix

display(IFrame('files/resources/ch03-linkedin/viz/cartogram.html', '100%', '600px'))
