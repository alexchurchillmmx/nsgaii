import random,math
import copy
from individual import Member

class Problem(object):

    def __init__(self, objectives, size_of_genotype):
        self.objectives = objectives
        self.num_objectives = len(self.objectives)
        self.size_of_genotype = size_of_genotype

    def set_random_genotype(self):
        pass
