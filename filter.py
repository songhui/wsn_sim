import config


class Filter(object):

    def __init__(self, env, rank=0,
                 selectivity_factor=1,
                 computational_cost=config.COMPUTATIONAL_COST):
        self.env = env
        self.rank = rank
        self.selectivity_factor = selectivity_factor
        self.computational_cost = computational_cost

    def execute():
        """
        This method executes the filter upon the node that it is currently
        running on. It decreases its host node's power availability, consumes
        the outgoing data buffer
        """
        pass
