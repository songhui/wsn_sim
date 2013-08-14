import config
from SimPy.Simulation import *
from random import uniform
from node import *

class Filter(Process):

    def __init__(self,
                 name,
                 computational_cost=config.COMPUTATIONAL_COST,
                 reportTo = None
                 ):
        Process.__init__(self)
        self.computational_cost = computational_cost
        self.reportTo = None        
        self.getDataFrom = set()
        self.data = None   
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

    def execute(self):
        """
        This method executes the filter upon the node that it is currently
        running on. It decreases its host node's power availability, consumes
        the outgoing data buffer
        """
        while True:
            yield passivate, self            
            if self.reportTo != None and self.data != None:
                self.transfer(self.reportTo, self.data)
                self.data = None
            
    def activateMe(self):
        activate(self, self.execute())


class Sink(Filter):
    
    def __init__(self,name):
        Filter.__init__(self,name)
        
    def execute(self):
        while True:
            yield passivate, self
            print "%s is outputing '%s' at %5.1f" %( self.name, self.data, now())
            
class SensorFilter(Filter):
    def __init__(self, name, sensor, reportTo):
        Filter.__init__(self, name = name, reportTo = reportTo)
        self.sensor = sensor
        self.sensor.host = self
    
    def activateMe(self):
        Filter.activateMe(self)
        self.sensor.activateMe()
            
class SensorSource(Process):
    
    def __init__(self, host = None, interval = 1):
        Process.__init__(self)
        self.host = host
        self.interval = interval
        
    def collectData(self):
        while True:
            yield hold, self, self.interval
            self.host.data = "A data born at %5.1f" % now()
            #print self.host.data
            reactivate(self.host)
    
    def activateMe(self):
        activate(self,self.collectData())
        





class Transferer(Process):
    def __init__(self):
        Process.__init__(self)
        self.data = None
    
    def setup(self, currentFilter, targetFilter, data):
        self.data = data
        self.targetFilter = targetFilter
        self.currentFilter = currentFilter
        
    def transf(self):
        while True:
            yield passivate, self
            if self.targetFilter.node == self.currentFilter.node:
                self.targetFilter.data = self.data
                reactivate(self.targetFilter)
            if self.targetFilter.node in self.currentFilter.node.neighbours: 
                yield hold, self, uniform(0,1)
                self.targetFilter.data = self.data
                reactivate(self.targetFilter)
    
    def activateMe(self):
        activate(self,self.transf())           
        
    
transfererPool = []    
def getAnIdleTransferer():
    #print 'pool size: %d' % len(transfererPool)
    try:
        trans = next(t for t in transfererPool if t.passive() )
        return trans
    except StopIteration:
        trans = Transferer()
        trans.activateMe()
        transfererPool.append(trans)
        return trans 