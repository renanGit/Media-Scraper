'''
Created on Jul 23, 2013

@author: killeriza
'''

import get_url as g

b = g.Build()
b.searchTitle('the negotiator')


t = b.getDetails()

print t