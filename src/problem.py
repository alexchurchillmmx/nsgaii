import random,math
import copy
from individual import Member
class Problem:
    num_objectives = 2
    size_of_genotype = 30
    
    def __init__(self):
        self.objectives = [self.objective_1,self.objective_2]
        self.num_objectives = len(self.objectives)
        self.fitness_max = self.initiate_fitness_minmax("max")
        self.fitness_min = self.initiate_fitness_minmax("min")

    def set_random_genotype(self):
        genotype = []
        for i in range(0,self.size_of_genotype):
            genotype.append(random.random())
        return genotype

    def initiate_fitness_minmax(self,min_or_max="min"):
        fitnesses = []
        if min_or_max == "min":
            base = 9999999.0
        else:
            base = 0.0
        for i in range(0,self.num_objectives):
            fitnesses.append(base)
        return fitnesses
        
    def reset_fitness_boundaries(self):
        self.fitness_max = self.initiate_fitness_minmax("max")
        self.fitness_min = self.initiate_fitness_minmax("min")
        
    def evaluate_boundary(self,member):
        for i,fitness in enumerate(member.fitness):
            if fitness > self.fitness_max[i]:
                self.fitness_max[i] = fitness
            if fitness < self.fitness_min[i]:
                self.fitness_min[i] = fitness
        
    def objective_1(self,member):
        return member.genotype[0]
        
    def objective_2(self,member):
        gx = self.g(member)
        #print "x =", x, "gx = ", gx, "x.genes[1] = ", x.genes[1]
        r = gx * (1.0 - math.sqrt(member.genotype[0] / gx))
        return r
        
    def g(self,member):
        sx = 0.0;
        for i in range(1, len(member.genotype)): # n genes numerated from 0
            sx += member.genotype[i]
        r = 1.0 + ((9.0 / (len(member.genotype) - 1.0))*sx)
        return r

    def mutation(self,member):
        # mutation_point = int(len(member.genotype) * random.random())
        # member.genotype[mutation_point] += random.uniform(-0.01,0.01)
        # if member.genotype[mutation_point] < 0:
            # member.genotype[mutation_point] = 0.0
        # elif member.genotype[mutation_point] > 1:
            # member.genotype[mutation_point] = 1.0
        for mutation_point in range(0,len(member.genotype)):
            if random.random() < 0.1:
                member.genotype[mutation_point] += random.uniform(-0.1,0.1)
                if member.genotype[mutation_point] < 0:
                    member.genotype[mutation_point] = 0.0
                elif member.genotype[mutation_point] > 1:
                    member.genotype[mutation_point] = 1.0
            
    def crossover(self,parent_1,parent_2):
        crossover_point = int(len(parent_1.genotype) * random.random())
        crossover_size = int((len(parent_1.genotype) - crossover_point) * random.random())
        child_1 = parent_2.copy()
        child_2 = parent_1.copy()
        for i in range(0,crossover_size):
            child_1.genotype[i+crossover_point] = parent_1.genotype[i+crossover_point]
            child_2.genotype[i+crossover_point] = parent_2.genotype[i+crossover_point]
        return [parent_1,parent_2]
    
    def get_successors(self,parent):
        successors = []
        for i,gene in enumerate(parent.genotype):
            child = parent.copy()
            genotype = copy.deepcopy(parent.genotype)
            if gene == True:
                genotype[i] = False
            else:
                genotype[i] = True
            child.genotype = genotype
            successors.append(child)
        return successors

if __name__ == "__main__":
    p = Problem()
    m_1 = Member(p)
    m_2 = Member(p)
    print(m_1)
    print(p.objective_1(m_1))
    print(p.objective_2(m_1))
    m_1.evaluate()
    print(m_1.fitness)
    for fitness in m_1.fitness:
        print('fitness:',fitness)
    print(m_2)
    print(p.objective_1(m_2))
    print(p.objective_2(m_2))
    m_2.evaluate()
    print(m_2.fitness)
    for fitness in m_2.fitness:
        print('fitness:',fitness)
    print('dominated:',m_1.dominated(m_2))