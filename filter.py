import config
from SimPy.Simulation import *
from random import uniform

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

    def execute(self):
        """
        This method executes the filter upon the node that it is currently
        running on. It decreases its host node's power availability, consumes
        the outgoing data buffer
        """
        while True:
            yield passivate, self            
            if self.reportTo != None and self.data != None:
                print "I'm %s" % self.name
                yield hold, self, uniform(2,5)
                self.reportTo.data = self.data
                self.data = None
                reactivate(self.reportTo)
            
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
    
    def __init__(self, host = None, interval = 10):
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
        

            
        
    
    
    