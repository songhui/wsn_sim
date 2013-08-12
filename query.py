import config


class Query(object):

    def __init__(self, 
                 name,
                 *filters
                 ):
        self.name = name
        self.filters = list(filters)
        

    def execute(self):
        """
        This method executes the filter upon the node that it is currently
        running on. It decreases its host node's power availability, consumes
        the outgoing data buffer
        """
        pass
  
 
class QueryInstance(object):
    """
        A Query Instance is the one maintained and spread by the nodes. It 
        has a reference to the Query(Type), and two cursors, *start* and *stop*.
        *start* is the filter the current node is
    """ 
    def __init__(self, query, start, stop):
        self.query = query
        self.start = start
        self.stop = stop