import config
from filter import *

class Node(Process):
    """The Node exemplifies a logical node in a WSN. It can accept
    mulitple filters to be added, from multiple queries. It has a notion of
    available computing power, remaining battery power, transmission cost to
    its parent, 
    (not yet:) incoming data buffer per query, and an outgoing data buffer
    per query
    A node receive data immediately without cost, but send data with a cost, 
    on both time and energy. Data are sent one by one, based on a token 
    """
    def __init__(self, name,
                 computing_ability=config.COMPUTATIONAL_POWER,
                 battery_power=config.BATTERY_POWER,
                 energy_cost_rate = config.DEFAUT_ENERGY_COST_RATE
                 ):
        Process.__init__(self)
        self.name = name
        self.computing_ability = computing_ability
        self.battery_power = battery_power
        self.energy_cost_rate = energy_cost_rate
        self.neighbours = set()
        self.filters = set()
        self.event = FireNodeEvent(name)
        self.rechargeEvent = SimEvent('recharge')
        self.transToken = Resource(capacity = 1, qType = FIFO, name = ('r_%s' % self.name))

    def addNeighbour(self, neighbour):
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)
        
    def removeNeighbour(self,neighbour):
        self.neighbours.remove(neighbour)
        neighbour.neighbours.remove(self)
        
    def consumePower(self, volumn):
        self.battery_power = self.battery_power - self.energy_cost_rate * volumn

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
            if self.battery_power <= 0:
                yield waitevent, self, self.rechargeEvent
                self.battery_power = 100  # let's suppose always fully recharge
                continue
            for filter in self.filters:
                data = self.event.data
                newdata = filter.filter(data, self.event.fromFilter)  
                if newdata == None: continue
                for n in (self.neighbours | set([self])):
                    if any((filter in f.getDataFrom) for f in n.filters):
                        transferer = getAnIdleTransferer()
                        transferer.setup(currentNode = self, targetNode = n, currentFilter = filter, data = newdata)
                        reactivate(transferer)
                   
    def activateMe(self):
        activate(self, self.execute())

    # End of class Node
        
class FireNodeEvent(SimEvent):
    '''
    A special event for a node to listen to data arriving.
    '''
        
    def __init__(self, name):
        SimEvent.__init__(self, name)
        self.fromFilter = None
        self.data = None
        
        
        
class SensorSource(Process):
    '''
    Generating data and put them to the host Node (the node is the actual sensor)
    '''
    
    def __init__(self, host = None, interval = 1):
        Process.__init__(self)
        self.host = host
        self.interval = interval
        
    def collectData(self):
        while True:
            yield hold, self, self.interval
            self.host.event.data = SensedData(name = ('e_%s' % self.host.name), volumn = 10)
            self.host.event.fromFilter = None
            #print self.host.data
            self.host.event.signal()
    
    def activateMe(self):
        activate(self,self.collectData())

    # End of SensorSource
    
class Transferer(Process):
    '''
    A transferer is in charge of one shot of data transfer from 
    one node to another. When a node wants to transfer a data, it
    get a new (actually idle) transferer, and ask it to do the 
    transfer for it (after asking, the node immediately goes back
    to listen to new incoming data)
    '''
    
    number = 0
    def __init__(self):
        Process.__init__(self)
        self.data = None
        self.isIdle = True
        self.name = Transferer.number
        Transferer.number = Transferer.number +1
    
    def setup(self, currentNode, targetNode, currentFilter, data):
        self.data = data
        self.currentNode = currentNode
        self.targetNode = targetNode
        self.currentFilter = currentFilter
        
    def transf(self):
        while True:
            self.isIdle = False
            if self.targetNode == self.currentNode:  # internal transfer
                yield hold, self, 0.1
                self.targetNode.event.data = self.data
                self.targetNode.event.fromFilter = self.currentFilter
                self.targetNode.event.signal()
            if self.targetNode in self.currentNode.neighbours: #external transfer     
                yield request, self, self.currentNode.transToken           
                yield hold, self, uniform(1,2)                
                self.targetNode.event.data = self.data
                self.targetNode.event.fromFilter = self.currentFilter
                self.currentNode.consumePower(self.data.volumn)
                self.targetNode.event.signal()
                yield release, self, self.currentNode.transToken
            self.isIdle = True   
            yield passivate, self
    
    def activateMe(self):
        activate(self,self.transf())           
        
    
transfererPool = []    
def getAnIdleTransferer():
    #print 'pool size: %d' % len(transfererPool)
    try:
        trans = next(t for t in transfererPool if t.isIdle )
        trans.isIdle = False
        return trans
    except StopIteration:
        trans = Transferer()
        trans.activateMe()
        transfererPool.append(trans)
        trans.isIdle = False
        return trans 
    
    
class SensedData(object):
    
    def __init__(self, name = 'some sensor', volumn = 0):
        self.name = name
        self.volumn = volumn
        self.bornTime = now()
        
    def __str__(self):
        return '<%s, born at %5.1f>' % (self.name, self.bornTime)