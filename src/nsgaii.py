from problem import Problem
from individual import Member
from fpconst import *
from list_recipes import normList
import math
import copy
import random

class NSGAII:
    mutation_rate = 1.0
    crossover_rate = 0.0
    generations = 200
    
    def __init__(self,problem,pop_size = 100):
        self.problem = problem
        self.population = []
        self.pop_size = pop_size
        self.seeding_pop_size = 100
        self.initialise_population()
        
    def initialise_population(self):
        for i in range(0,self.seeding_pop_size):
            p = Member(self.problem)
            self.population.append(p)
        self.evaluate_population()
        
    def evaluate_population(self,population=[]):
        if population == []:
            population = self.population
        for member in population:
            member.evaluate()

    def fast_nondominated_sort(self, population=[]):
        # dictionary, S, containing the solutions that an individual dominates
        S = dict()
        if population == []:
            population = self.population # note: fix
        fronts_list = [[] for m in population]
        # init population
        for member in population:
            # number of solutions member dominated by n_member
            member.n = 0
            S[hash(member)] = []
        # calculate #dominations
        for member in population:
            for other_member in population:
                # create entry for member in S, S_member
                if member.dominates(other_member):
                    S[hash(member)].append(other_member)
                    other_member.n += 1
        # create non-dominated front
        for member in population:
            # member is nondominated
            if member.n == 0:
                member.domination_index = 0
                fronts_list.append([])
                # add to first front
                fronts_list[0].append(member)
        i = 0
        # note: fix
        while len(fronts_list[i]) != 0:
            front = []
            for member in fronts_list[i]:
                for dominated_member in S[hash(member)]:
                    dominated_member.n -= 1
                    if dominated_member.n == 0:
                        dominated_member.domination_index = i + 1
                        front.append(dominated_member)
            i += 1
            fronts_list.append([])
            fronts_list[i] = front
        return fronts_list

    def crowding_distance_assignment(self, front, to_print = False):
        len_front = len(front)
        if len_front > 0:
            # Initialize distance for each individual
            for x in front:
                x.crowded_distance = 0
            # iterate through each objective and add to CD for each individual
            for objective in range(0, self.problem.num_objectives):
                # Sort using objective
                front = sorted(front,key=lambda member: member.fitness[objective])
                normalised_front = []
                for member in front:
                    normalised_front.append(member.fitness[objective])
                try:
                    normalised_front = normList(normalised_front)
                except:
                    # stops ZeroDivision errors
                    for i in range(0,len(normalised_front)):
                        normalised_front[i] = 0.0
                for i,member in enumerate(front):
                    member.normalised_fitness[objective] = normalised_front[i]
                # Boundary points are always selected
                front[0].crowded_distance = PosInf
                front[len_front - 1].crowded_distance = PosInf
                for i in range(1, len_front - 1):
                    front[i].crowded_distance += (front[i + 1].normalised_fitness[objective] -
                                                  front[i - 1].normalised_fitness[objective])

    def binary_tournament(self,population):
        parent_a = random.choice(population).copy() # note: fix
        parent_b = random.choice(population).copy()
        return self.crowded_comparison(parent_a,parent_b)
        
    def crowded_comparison(self,parent_a,parent_b):
        if parent_a.domination_index < parent_b.domination_index:
            return parent_a
        elif parent_b.domination_index < parent_a.domination_index:
                return parent_b
        elif parent_a.crowded_distance > parent_b.crowded_distance:
            return parent_a
        else:
            return parent_b

    def run(self):
        # step 1: an initial population has been created already
        population = self.population
        # step 2: non dominated sort
        fronts = self.fast_nondominated_sort(population)
        self.print_fronts(fronts)
        for f in fronts:
            self.crowding_distance_assignment(f)
        print('#############initial population###########')
        self.print_population(population)
        print('///#############initial population###########///')
        gen = 0
        while gen < self.generations:
            print('gen:',str(gen))
            self.print_fronts(fronts,True,gen)
            # step 3: create child population
            child_population = []
            while len(child_population) < self.pop_size:
                parent_a = self.binary_tournament(population)
                child = parent_a.copy()
                if random.random() < self.crossover_rate:
                    parent_b = self.binary_tournament(population)
                    children = child.crossover(parent_b)
                else:
                    children = [child]
                for child_to_mutate in children:    
                    if random.random() < self.mutation_rate:
                        child_to_mutate.mutation()
                while len(child_population) < self.pop_size and len(children) > 0:
                    child_population.append(children.pop())

            # evaluate child population
            self.evaluate_population(child_population)
            # merge with original
            population_R = population + child_population
            # determine fronts
            fronts = self.fast_nondominated_sort(population_R)
            # set crowding distance
            for f in fronts:
                self.crowding_distance_assignment(f,to_print=False)
            new_population = []

            for f in fronts:
                if (len(new_population) > self.pop_size):
                    break
                elif (len(new_population) + len(f)) < self.pop_size:
                    new_population += f
                else:
                    f = sorted(f, key=lambda member: -member.crowded_distance)
                    while len(new_population) < self.pop_size and len(f) > 0:
                        new_population.append(f.pop())
            fronts = self.fast_nondominated_sort(new_population)
            for f in fronts:
                self.crowding_distance_assignment(f) # note: fix
            population = new_population
            gen += 1
        print('#############final population###########')
        self.print_population(population)
        self.print_fronts(fronts,True,gen)
        
    def print_population(self,population=[]):
        if population == []:
            population = self.population
        print("-"*10)
        population = sorted(population,key=lambda member: member.domination_index)
        for i,p in enumerate(population):
            print("["+str(i)+"] " + str(p) + "   di = " +str(p.domination_index) + "   cd = "+str(p.crowded_distance)+"   fitness = "+str(p.fitness))
            
    def print_fronts(self,fronts,print_to_file=False,gens=0):
        string = ""
        for i,f in enumerate(fronts):
            if len(f) > 0:
                if i % 3 == 0:
                    color = 'b'
                elif i % 3 == 1:
                    color = 'r'
                else:
                    color = 'g'
                front_text_x = "front_x_"+str(i)+" = ["
                x_var = "front_x_"+str(i)
                y_var = "front_y_"+str(i)
                front_text_y = "front_y_"+str(i)+" = ["
                for m in f:
                    front_text_x += (str(m.fitness[0]) + ",")
                    front_text_y += (str(m.fitness[1]) + ",")
                front_text_x += "];"
                front_text_y += "];"
                if print_to_file:
                    string += (front_text_x)
                    string += (front_text_y)
                    string += ("plot("+x_var+","+y_var+",\'"+color+"x\');")
                else:
                    print(front_text_x)
                    print(front_text_y)
                    print("plot("+x_var+","+y_var+",\'"+color+"x\');")
        if print_to_file:
            file = open('results/all_fronts_'+str(gens)+'.dat','w')
            file.write(string)
            file.close()
                
    def depth_first_search(self):
        open_list = []
        parent = Member(self.problem)
        open_list.append(parent)
        path = []
        while len(open_list) > 0:
            parent = open_list.pop(0)
            path.append(parent)
            print(len(path))
            successors = self.problem.get_successors(parent)
            for successor in successors:
                is_in_path = self.in_path(successor,path)
                #is_in_path = False
                is_in_open_list = self.in_open_list(successor,open_list)
                if is_in_path == False and is_in_open_list == False:
                    open_list.append(successor)
        self.evaluate_population(path)
        fronts = self.fast_nondominated_sort(path)
        self.print_fronts(fronts,True)
        print(len(path))
        
    def in_path(self,parent,path):
        for p in path:
            if str(parent.genotype) == str(p.genotype):
                return True
        return False

    def in_open_list(self,parent,open_list):
        for p in open_list:
            if str(parent.genotype) == str(p.genotype):
                return True
        return False

if __name__ == "__main__":
    p = Problem()
    ns = NSGAII(p,100)
    ns.run()
