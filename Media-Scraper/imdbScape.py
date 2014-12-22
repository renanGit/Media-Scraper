'''
Created on Jul 23, 2013

@author: Renan Santana
'''

import get_url as g

b = g.Build()
b.searchTitle('the negotiator')


t = b.getDetails()

print t