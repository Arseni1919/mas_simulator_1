from GLOBALS import *


class AlgMeta(abc.ABC):
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def reset(self, agents_list, field_list, *args, **kwargs):
        pass

    @abc.abstractmethod
    def iteration_calc(self, observations, env, *args, **kwargs):
        pass


