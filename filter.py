import config


class Filter(object):

    def __init__(self,
                 computational_cost=config.COMPUTATIONAL_COST
                 ):
        self.computational_cost = computational_cost

    def execute(self):
        """
        This method executes the filter upon the node that it is currently
        running on. It decreases its host node's power availability, consumes
        the outgoing data buffer
        """
        pass
