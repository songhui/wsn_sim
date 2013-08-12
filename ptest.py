'''
Created on Aug 12, 2013

@author: Hui
'''

def funtest(*args):
    lists = list(args)
    lists.append(10)
    print lists

t = [5,6,7]  
funtest(*t)

print t


def fun2(arg):
    a = list(arg)
    a.append(5)
    
t = [5,6]

fun2(t)

print t
