'''
@author: Alex
'''
import copy
class Member:
    domination_index = 0 # front individual is in
    crowded_distance = 0 # measure of diversity in front
    n = 0 # number of individuals dominating
    def __init__(self,problem,genotype=[]):
        self.problem = problem
        self.genotype = genotype
        self.fitness = []
        self.normalised_fitness = []
        for objective in range(0,self.problem.num_objectives):
            self.fitness.append([0])
            self.normalised_fitness.append([0])
        if genotype == []:
            self.set_random_genotype()
            
    def set_random_genotype(self):
        self.genotype = self.problem.set_random_genotype()
        return self.genotype
                
    def dominates(self,other):
        dominated = False
        all_functions_equal_or_smaller_than_self = True
        at_least_one_function_better_than_other = False
        for i in range(0, self.problem.num_objectives):
            if self.fitness[i] > other.fitness[i]:
                all_functions_equal_or_smaller_than_self = False
            if self.fitness[i] < other.fitness[i]:
                at_least_one_function_better_than_other = True
            
        if all_functions_equal_or_smaller_than_self == True and at_least_one_function_better_than_other == True:
            # if no objective is larger in the other
            dominated = True
        return dominated
    
    def evaluate(self):
        for i in range(0,len(self.problem.objectives)):
            self.fitness[i] = self.problem.objectives[i](self)
            
    def mutation(self):
        self.problem.mutation(self)
        
    def crossover(self,other_parent):
        return self.problem.crossover(self,other_parent)
    
    def copy(self):
        new_member = Member(problem = self.problem,genotype=copy.deepcopy(self.genotype))
        new_member.fitness = copy.deepcopy(self.fitness)
        new_member.normalised_fitness = copy.deepcopy(self.normalised_fitness)
        new_member.domination_index = copy.deepcopy(self.domination_index)
        new_member.crowded_distance = copy.deepcopy(self.crowded_distance)
        return new_member
    
    def equals(self,other):
        if str(self) == str(other):
            return True
        else:
            return False
        
    def __str__(self):
        string = ""
        for gene in self.genotype:
            if gene:
                string+=str(gene)
            else:
                string+=str(gene)
        return string
        
if __name__ == "__main__":
    pass
    