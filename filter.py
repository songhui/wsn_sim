import config
from SimPy.Simulation import *
from random import uniform
from node import *

class Filter():

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

    def execute(self):
        """
        This method executes the filter upon the node that it is currently
        running on. It decreases its host node's power availability, consumes
        the outgoing data buffer
        """
#         while True:
#             yield passivate, self            
#             if self.reportTo != None and self.data != None:
#                 self.transfer(self.reportTo, self.data)
#                 self.data = None
            
    def activateMe(self):
        activate(self, self.execute())


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
            


        
        





