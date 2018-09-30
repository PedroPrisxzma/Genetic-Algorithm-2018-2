import tree
import random
from copy import deepcopy
from math import sqrt, log, exp
import pandas
from functools import reduce

# Implements the Ramped half_and_half
def half_and_half(pop_size, max_depth, x_nums):
    population = [] # our final Individuals list
# Separates population in groups, each group being half grow and half full trees
# Total of max_depth-1 groups, for trees with sizes from (2, ..., max_depth)
    indv_pop = [] # Individuals per population
    indv_left = deepcopy(pop_size) # Individuals left to assign
    if(max_depth == 1):
        indv_pop.append(pop_size)
        indv_left = 0

    for i in range(0,max_depth-1):
        indv_pop.append(0)

    i = 0
    while(indv_left > 0):
        if(i == max_depth-1):
            i = 0
        indv_pop[i] = indv_pop[i]+1
        indv_left = indv_left -1
        i = i+1

# initial depth level
    depth_level = 2
    for i in range(len(indv_pop)):
        if(max_depth == 1): # Corrects the case when only the root exists
            depth_level = 1
        if(indv_pop[i] > 0):
            try:
                grow_type = indv_pop[i] // 2
                full_type = indv_pop[i] // 2
            except:
                print('Error on population group', i, ' with a size of ', indv_pop[i])
# Ajust population on odd population sizes
            if((indv_pop[i] % 2 )> 0):
                grow_type = grow_type + 1
            for i in range(full_type):
                population.append(tree.full_tree(0, int(depth_level), x_nums))
            for i in range(grow_type):
                population.append(tree.grow_tree(0, int(depth_level), x_nums))
            depth_level = depth_level + 1
    return population


# Build tree value
def tree_val(x_vals, nivel, tree):
    if(tree.children == []):
        #print('VARS')
        for i in range(len(x_vals)):
        #    print('x'+str(i), tree.value)
            if(tree.value == ('x' + str(i))):
        #        print('aaaaaaaaa')
    #            print(x_vals[i][nivel])
                return (x_vals[i][nivel])
        #        print("VARS")
    #    print("VARS2")
        return(tree.value)

    elif(tree.value == '+'):
        child_0 = deepcopy(tree_val(x_vals, nivel, tree.children[0]))
        child_1 = deepcopy(tree_val(x_vals, nivel, tree.children[1]))
        #print('op +')
        #print(child_0)
        #print(child_1)
        tree_value = deepcopy(child_0 + child_1)
    elif(tree.value == '-'):
        child_0 = deepcopy(tree_val(x_vals, nivel, tree.children[0]))
        child_1 = deepcopy(tree_val(x_vals, nivel, tree.children[1]))
        #print('op -')
        #print(child_0)
        #print(child_1)
        tree_value = deepcopy(child_0 - child_1)
    elif(tree.value == '*'):
        child_0 = deepcopy(tree_val(x_vals, nivel, tree.children[0]))
        child_1 = deepcopy(tree_val(x_vals, nivel, tree.children[1]))
        #print('op *')
        #print(child_0)
        #print(child_1)
        tree_value = deepcopy(child_0 * child_1)
    elif(tree.value == '/'):
        aux = deepcopy(tree_val(x_vals, nivel, tree.children[1]))
        #print('op /')
        #print(aux)
        if(aux != 0):
            tree_value = deepcopy(tree_val(x_vals, nivel, tree.children[0]) / aux)
        else:
            tree_value = deepcopy(0)
    elif(tree.value == '**2'):
        try:
            tree_value = deepcopy(tree_val(x_vals, nivel, tree.children[0]) ** 2)
        except:
            tree_value = 999999
    elif(tree.value == 'sqrt'):
        aux = deepcopy(tree_val(x_vals, nivel, tree.children[0]))
        #print('op sqrt')
        #print(aux)
        if(aux >= 0):
            tree_value = deepcopy(sqrt(aux))
        else:
            tree_value = deepcopy(999999)
    elif(tree.value == 'log'):
        aux = deepcopy(tree_val(x_vals, nivel, tree.children[0]))
        #print('op log')
        #print(aux)
        if(aux > 0):
            tree_value = deepcopy(log(aux))
        else:
            tree_value = deepcopy(999999)
    return tree_value



# Changing and OffSpring Functions
def new_gene(tree_X, tree_Y=None, mode='crossover', x_nums=0):
    new_tree_X = deepcopy(tree_X)
    new_tree_Y = deepcopy(tree_Y)
    # Node Types

    binary = ['+', '-', '*', '/']
    unary = ['log', 'sqrt', '**2']

# Crossover mode
    if(mode == 'crossover'):
        type_Y = -1
        type_X = -2
        while(type_X != type_Y):
            node_X = (random_node(random.randrange(1, 7, 1), new_tree_X))
            node_Y = (random_node(random.randrange(1, 7, 1), new_tree_Y))
            if( (node_X.level == node_Y.level)):
                type_X = 1
                type_Y = 1
            #print('tried')
            #print(node_X)
            #print(node_Y)
        #print('Match '+str(type_Y)+' '+str(type_X))
        #print(node_X)
        #print(node_Y)
        aux = deepcopy(node_X)
        node_X.parent[0][0].children[node_X.parent[0][1]] = node_Y
        node_Y.parent[0][0].children[node_Y.parent[0][1]] = aux
        #new_tree_X.level_update()
        #new_tree_Y.level_update()
        return(new_tree_X, new_tree_Y)
# Mutation mode
# OBS: A mutacao pode resultar no mesmo operado/terminal
    elif(mode == 'mutation'):
        node_X = (random_node(random.randrange(0, 8, 1), new_tree_X))
        if((node_X.value not in unary) and (node_X.value not in binary) ):
            coin = random.randrange(0, x_nums,1)
            num = round(random.uniform(0,1), 4)
            var = 'x'
            #print("mutation")
            #print(node_X.value)
            node_X.value = (var+str(coin) if(coin==0) else num)
            #print(node_X.value)

        elif(node_X.value in unary):
            op = random.randrange(0,3,1)
            #print("mutation")
            #print(node_X.value)
            node_X.value = unary[op]
            #print(node_X.value)

        elif(node_X.value in binary):
            op = random.randrange(0,4,1)
            #print("mutation")
            #print(node_X.value)
            node_X.value = binary[op]
            #print(node_X.value)
        return(new_tree_X)
# Returns random node value, an aux function
def random_node(steps, tree):
    if(tree.children == []):
        return(tree)
    elif(steps == 0):
        return(tree)
    else:
        coin = random.randrange(0, len(tree.children), 1)
        aux = (random_node(steps-1, tree.children[coin]))
    return(aux)

# Fitness calculator (returns fitness for a given entry)
def fitness(x_vals, y_vals, tree):
    numerador = 0
    denominador = 0
    media_saida = (reduce(lambda x, y: x + y, y_vals)/ len(y_vals))
    for i in range(len(y_vals)):
        for j in range(len(x_vals)):
            try:
                numerador = (numerador + ((y_vals[i] - tree_val(x_vals, i, tree))**2))
            except:
                numerador = 1.7976931348623157e+308
        denominador = (denominador + ((y_vals[i] - media_saida)**2))
    #print('numerador', numerador)
    #print('denominador', denominador)

    fit = (numerador/denominador)
    if(fit < 0):
        fit = 0
    return(sqrt(fit) if(denominador != 0) else 0)

def evolution_cycle(old_gen, max_gen, pop_size, k_tournament, mut_chance, cross_chance, elite, x_nums, x_vals, y_saida):
    old = old_gen
    best_of_gens = [] # Melhor fitness por geracao
    worse_of_gens = [] # Pior fitness por geracao
    mean_of_gens = [] # Media da fitness por geracao
    filhos_mm_pais = [] # Numero de filhos com media melhor que os pais por geracao
    repeats = [] # Numero de individuos repetidos na geracao
    for gen in range(0, int(max_gen)):
        #print('gen = ', gen)
        # Tournament selection
        filhos_mm_pais.append(0)
        repeats.append(0)
        next_gen = []
        while(len(next_gen) != int(pop_size)):
        #    print(old, k_tournament)
            participants = random.sample(old, int(k_tournament))
            # Pick pai
            pai = participants[0]
            for t in participants:
                if(pai.fit < t.fit):
                    pai = t
            # Apply Mutation
            coin = random.randint(0,10)/10
            if(coin < float(mut_chance)):
                filho = new_gene(pai, mode='mutation', x_nums=x_nums)
                filho.fit = fitness(x_vals, y_saida, filho)
                if(elite == 'no'):
                    next_gen.append(filho)
                else:
                    next_gen.append(filho if(filho.fit < pai.fit) else pai)

            # No mutation? Try Crossover
            else:
                participants2 = random.sample(old, int(k_tournament))
                # Pick mae
                mae = participants2[0]
                for t in participants2:
                    if(mae.fit < t.fit):
                        mae = t
                # Apply Crossover
                coin = random.randint(0,10)/10
                if(coin < float(cross_chance)):
                    filhos = new_gene(pai, mae, x_nums=x_nums)
                    filhos[0].fit = fitness(x_vals, y_saida, filhos[0])
                    filhos[1].fit = fitness(x_vals, y_saida, filhos[1])
                    media_fit_pais = (pai.fit + mae.fit / 2)
                    # Quantos filhos tem fitness melhor doq a media dos pais
                    filhos_mm_pais[gen] = (filhos_mm_pais[gen]+1 if(filhos[0].fit > media_fit_pais) else(filhos_mm_pais[gen]))
                    filhos_mm_pais[gen] = (filhos_mm_pais[gen]+1 if(filhos[1].fit > media_fit_pais) else(filhos_mm_pais[gen]))

                    if(elite == 'no'):
                        next_gen.append(filhos[0])
                        next_gen.append(filhos[1])
                    else:
                        pick_2 = [pai, mae, filhos[0], filhos[1]]
                        best_2 = sorted(pick_2, key=lambda x: x.fit)
                        next_gen.append(best_2[0])
                        next_gen.append(best_2[1])
            if(len(next_gen) > int(pop_size)):
                next_gen = next_gen[:int(pop_size)]
        old = deepcopy(next_gen)
        next_gen = sorted(next_gen, key=lambda x: x.fit)

        for ind in range(len(next_gen)-1):
            if(next_gen[ind] == next_gen[ind+1]):
                repeats[gen] = repeats[gen]+1

        best_of_gens.append(next_gen[0])
        #print('Best gen ', gen, next_gen[0].fit)
        worse_of_gens.append(next_gen[int(pop_size)-1])

    return(next_gen, best_of_gens, worse_of_gens, filhos_mm_pais, repeats)

######################################### NOT TESTED ###########################
