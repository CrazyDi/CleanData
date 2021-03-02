import pandas as pd

import cleandata.basicdescriptive as bd


nls97 = pd.read_csv('data/nls97f.csv')

print(bd.get_count(nls97, ['maritalstatus','gender','colenroct00']))
