import config


class Node(object):
    """The Node exemplifies a logical node in a WSN. It can accept
    mulitple filters to be added, from multiple queries. It has a notion of
    available computing power, remaining battery power, transmission cost to
    its parent, incoming data buffer per query, and an outgoing data buffer
    per query
    """
    def __init__(self, env, name, queries,
                 computing_ability=config.COMPUTATIONAL_POWER,
                 battery_power=config.BATTERY_POWER
                 ):
        self.env = env
        self.name = name
        self.queries = queries
        self.computing_ability = computing_ability
        self.battery_power = battery_power

    def add_query(self, query):
        self.queries += query

    def remove_query(self, query):
        self.queries[:] = [qry for qry in self.queries
                           if not qry.name == query.name]

    def execute_queries(self):
        for query in self.queries:
            self.execute(query)

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
