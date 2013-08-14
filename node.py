import config
from filter import *

class Node(object):
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
        self.name = name
        self.computing_ability = computing_ability
        self.battery_power = battery_power
        self.neighbours = set()
        self.filters = set()

    def addNeighbour(self, neighbour):
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)
        
    def removeNeighbour(self,neighbour):
        self.neighbours.remove(neighbour)
        neighbour.neighbours.remove(self)
        
    

    def execute(self, query):
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
