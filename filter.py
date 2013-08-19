import config
from SimPy.Simulation import *
from random import uniform
from node import *

class Filter():
    
    '''
    Filters only transform the data, 
    (later) should consume some energy.
    '''

    def __init__(self,
                 name,
                 computational_cost=config.COMPUTATIONAL_COST,
                 reportTo = None
                 ):
        self.dirty = False  # whether this filter got data processed or not
        self.computational_cost = computational_cost
        self.reportTo = None        
        self.getDataFrom = set()  
        self.name = name     
        if reportTo != None:
            self.setReportTo(reportTo)
        self.node = None
    
    def setNode(self, node):
        self.node = node
        node.filters.add(self)
        
    def setReportTo(self, filter):        
        self.reportTo = filter
        try:
            filter.addGetDataFrom(self)
        except AttributeError:
            pass
    
    def addGetDataFrom(self, filter):  
        if filter.reportTo != self:
            filter.reportTo = self
        self.getDataFrom.add(filter) 
        
    def transfer(self, target, data):
        transferer = getAnIdleTransferer()
        transferer.setup(currentFilter = self, targetFilter = target, data = data)
        reactivate(transferer)
        
    def filter(self, data, fromFilter):
        if not fromFilter in self.getDataFrom:
            return None
        self.dirty = True
        return self._filter(data)
        
    def _filter(self, data):  #default impl, do not change data at all
        return data




class Sink(Filter):
    
    def __init__(self,name):
        Filter.__init__(self,name)
        
    def _filter(self, data):
         print "%s is outputing '%s' at %5.1f" %( self.name, data, now())
         return None
        
#     def execute(self):
#         while True:
#             yield passivate, self
#             print "%s is outputing '%s' at %5.1f" %( self.name, self.data, now())
            


        
        





