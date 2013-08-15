import config
from filter import *

class Node(Process):
    """The Node exemplifies a logical node in a WSN. It can accept
    mulitple filters to be added, from multiple queries. It has a notion of
    available computing power, remaining battery power, transmission cost to
    its parent, incoming data buffer per query, and an outgoing data buffer
    per query
    """
    def __init__(self, name,
                 computing_ability=config.COMPUTATIONAL_POWER,
                 battery_power=config.BATTERY_POWER
                 ):
        Process.__init__(self)
        self.name = name
        self.computing_ability = computing_ability
        self.battery_power = battery_power
        self.neighbours = set()
        self.filters = set()
        self.event = FireNodeEvent(name)

    def addNeighbour(self, neighbour):
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)
        
    def removeNeighbour(self,neighbour):
        self.neighbours.remove(neighbour)
        neighbour.neighbours.remove(self)
        
    

    def execute(self):
        """
        In this method, all the filters pertaining to a particular query are
        executed in rank-order, i.e., the lowest ranked filter gets executed
        first.
        The filter itself only operates on the outgoing data buffer of the node
        since multiple filters may have to work on the same data. To do this,
        the node first consumes all of its incoming data buffer, and inserts
        the data into the outgoing buffer (do we need this? Can every operation
                                           not be done on the same buffer?)
        """
        while True:
            yield waitevent, self, self.event
            for filter in self.filters:
                newdata = filter.filter(self.event.data, self.event.fromFilter)  
                if newdata == None: continue
                for n in (self.neighbours | set([self])):
                    transferer = getAnIdleTransferer()
                    transferer.setup(currentNode = self, targetNode = n, currentFilter = filter, data = newdata)
                    reactivate(transferer)
                     
    def activateMe(self):
        activate(self, self.execute())

        
class FireNodeEvent(SimEvent):
    
    def __init__(self, name):
        SimEvent.__init__(self, name)
        self.fromFilter = None
        self.data = None
        
class SensorSource(Process):
    
    def __init__(self, host = None, interval = 1):
        Process.__init__(self)
        self.host = host
        self.interval = interval
        
    def collectData(self):
        while True:
            yield hold, self, self.interval
            self.host.event.data = "A data born at %5.1f" % now()
            self.host.event.fromFilter = None
            #print self.host.data
            self.host.event.signal()
    
    def activateMe(self):
        activate(self,self.collectData())

class Transferer(Process):
    def __init__(self):
        Process.__init__(self)
        self.data = None
    
    def setup(self, currentNode, targetNode, currentFilter, data):
        self.data = data
        self.currentNode = currentNode
        self.targetNode = targetNode
        self.currentFilter = currentFilter
        
    def transf(self):
        while True:
            yield passivate, self
            if self.targetNode == self.currentNode:
                yield hold, self, 0.1
                self.targetNode.event.data = self.data
                self.targetNode.event.fromFilter = self.currentFilter
                self.targetNode.event.signal()
            if self.targetNode in self.currentNode.neighbours: 
                yield hold, self, uniform(1,2)
                self.targetNode.event.data = self.data
                self.targetNode.event.fromFilter = self.currentFilter
                self.targetNode.event.signal()
    
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