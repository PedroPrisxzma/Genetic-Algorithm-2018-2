import random
from copy import deepcopy

# The tree class
class node(object):
    def __init__(self, value, level=0, fit=0, children = [], parent=[]):
        self.value = value
        self.fit = fit
        self.children = children
        self.parent = parent
        self.level = level

    def __str__(self, level=0): # prints out the tree
        ret = "\t"*level+repr(self.value)+'('+repr(self.level)+')'+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def add_child(self, no): # Adds child node
        self.children.append(no)

    def level_update(self, level=0): # Updates node depth_level
        self.level = level
        for child in self.children:
            child.level_update(level=level+1)

    def max_level(self): # Finds maximum tree depth from a node
        if(len(self.children) == 1):
            a = deepcopy(self.children[0].max_level())
            return( a)
        elif(len(self.children) == 2):
            a = deepcopy(self.children[0].max_level())
            b = deepcopy(self.children[1].max_level())
            return( a if a > b else b)
        else:
            return( self.level )

    def __repr__(self):
        return '<tree node representation>'


############################# Basic funtions used #############################
# Return a random integer, operator or 'variable(x or y)'
def r_node(x_nums, mode = 0): # x_nums is the number of dif variables
    if(mode == 0): #When not a leaf
        coin = 2

    elif(mode == 2): # One input operator
        op_list = ['log', 'sqrt', '**2']
        op = random.randrange(0,3,1)
        return(op_list[op])
    else: #When a leaf
        coin = random.randrange(0,2,1)
    # returns a random int
    if(coin == 0):
        return(round(random.uniform(0,1), 4)) #might change the max/min limit
    #returns a random variable
    elif(coin == 1):
        x_ = random.randrange(0,x_nums,1)
        return('x'+str(x_))
    #returns a random binary operator
    elif(coin == 2):
        op_list = ['+', '-', '*', '/']
        op = random.randrange(0,4,1)
        return(op_list[op])

# Builds a Grow tree method
def grow_tree(size, max_size, x_nums):
    # Case root
    if(size == 0):
        no = deepcopy(node(value=r_node(x_nums), level=size))
        for i in range(2):
            no.add_child(grow_tree(size+1, max_size, x_nums))
            no.children[i].parent.append((no,i))

    # Case middle node
    elif(size < max_size):
        coin = random.randrange(0,2,1)
        if(coin == 0):
            no = deepcopy(node(value=r_node(x_nums, 'leaf'), level=size))
        else:
            type = random.randrange(0,2,1)
            if(type == 0): # Operador unario
                no = deepcopy(node(value=r_node(x_nums, mode=2), level=size))
                for i in range(1):
                    no.add_child(grow_tree(size+1, max_size, x_nums))
                    no.children[i].parent.append((no,i))
            else: # Operador binario
                no = deepcopy(node(value=r_node(x_nums), level=size))
                for i in range(2):
                    no.add_child(grow_tree(size+1, max_size, x_nums))
                    no.children[i].parent.append((no,i))
    # Case Leaf
    elif(size >= max_size):
        no = deepcopy(node(value=r_node(x_nums, 'leaf'), level=size))
    return no

# Builds a full tree method
def full_tree(size, max_size, x_nums):
    # Case not a leaf
    if(size < max_size):
        type = random.randrange(0,2,1)
        if(type == 0): # Operador unario
            no = deepcopy(node(r_node(x_nums, mode=2), level=size))
            for i in range(1):
                no.add_child(full_tree(size+1, max_size, x_nums))
                no.children[i].parent.append((no,i))
        else: # Operador binario
            no = deepcopy(node(value=r_node(x_nums), level=size))
            for i in range(2):
                no.add_child(full_tree(size+1, max_size, x_nums))
                no.children[i].parent.append((no,i))

    # Case Leaf
    else:
        no = deepcopy(node(value=r_node(x_nums, 'leaf'), level=size))
    return no
