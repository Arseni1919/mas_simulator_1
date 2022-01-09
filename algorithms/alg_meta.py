from GLOBALS import *


class AlgMeta(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def reset(self, agents_list, field_list):
        pass

    @abc.abstractmethod
    def iteration_calc(self, observations, env):
        pass


