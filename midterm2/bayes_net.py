# bayes network class
import numpy as np
import random
import networkx as nx
import graphviz 

# DONE: implement automatic graph generation - need to be acyclic 
# DONE: implement topological order of nodes
# DONE: implement graphical representation of network
# DONE: use graph networkx to do all the work on graph
# DONE: check acyclicity of graph
# DONE: COVID example (MANDATORY)
# DONE: DAILY ROUTINE example (MANDATORY)
# TODO: CONSIDERATIONS
# DONE: add readme 
# DONE: fix graph drawing


class BayesNetwork:
    
    def __init__(self, nodes: dict, values: list):
        """Bayes network data structure, undirected by default.
    
            Args:
                nodes (dict): Dictionary of nodes. Each node is a BNode object.
                values (list): List of values that each node can take. Ex: ['True', 'False'] for binomial, [0,1,2,3] for multinomial.
        """
        self.nodes = nodes
        self.values = values 
        G = nx.DiGraph(self.get_edges())

        # check acyclicity of graph
        if nx.is_directed_acyclic_graph(G): self.g = G
        else: raise ValueError('Network is not acyclic.')

        # add nodes without edges to the graph
        for node in self.get_nodes():
            if node not in self.g.nodes: self.g.add_node(node)

    def get_nodes(self):
        return list(self.nodes.keys())
    
    def get_edges(self):
        edges = []
        for key,node in self.nodes.items():
            if node.get_parents() != None:
                for parent in node.get_parents():
                    edges.append((parent,key))
        return edges   
    
    def bi_choice(self, probability : int, seed : int) -> str:
        """ Return True or False according to a given probability.

            Args:
                probability (int): probability of True.
                seed (int): random seed to repeat same sampling.
        """
        if seed != None: random.seed(seed)
        if random.random() < probability: return 'True'
        else: return 'False'

    def multi_choice(self, values: list, probabilities : list, seed : int = None) -> str:
        """ Return a value from a list according to its probability distribution.
        
            Args:
                values (list): list of values that each node can take.
                probabilities (list): list of probabilities of each value.
                seed (int): random seed to repeat same sampling.

            Returns:
                str: a value from the list of values
        """
        if (len(values)!=len(probabilities)): raise ValueError('Length of values and probabilities must be the same.')

        if seed != None: random.seed(seed)

        return np.random.choice(values,p=probabilities)

    def sampling (self, n=1, init: dict = {}, seed: int = None) -> dict:
        """ Ancestral sampling n times from the network.
        
        Args:
            n (int): number of times to sample.
            init (dict): initial state of the network.
            seed (int): random seed.

        Returns:
            dict: n samples
        """
        samples={} # n samples

        print('Ancestral sampling %d times from the network...' %(n))
        print()

        # DONE: topological order of nodes
        nodes = list(nx.topological_sort(self.g))
        print('Topological ordering of nodes: ', end="")
        print(nodes)
        print()

        for iter in range(n):
            s = {} # i-esimo sample
            for nname in nodes: # get node in topological order
                
                node = self.nodes[nname]

                #check init state
                if nname in init:
                    s[nname] = init[nname]
                else:
                    # get cpt of node
                    cpt = node.get_cpt() # cpt of the current node
                    
                    # get parents of node
                    parents = node.get_parents()

                    if parents == None: 
                        s[nname] = self.multi_choice(self.values, cpt['p'])
                    else:
                        s[nname] = self.multi_choice(self.values, cpt[tuple([s[parent] for parent in parents])])
                            
            # add current sampling to samples
            samples[iter+1] = s
        
        return samples 

    # estimate P(X=x|e) from samples agreeing with e
    def estimate(self, X: str, x: str, e: dict, samples: dict) -> dict:
        """ Estimate the probability of a node given a set of evidences.
        
        Args:
            X (str): node to estimate.
            x (str): value of X.
            e (dict): evidences.
            samples (dict): samples from the network.

        Returns:
            dict: probability distribution of X given e.
        """
        # count samples that agree with e
        count = 0
        for s in samples.values():
            if all(s[key] == value for key, value in e.items()): count += 1
        
        # count samples that agree with e and X
        count_X = 0
        for s in samples.values():
            if all(s[key] == value for key, value in e.items()) and s[X] == x: count_X += 1

        # estimate probability
        if count == 0: p = 0
        else: p = count_X/count

        return {X: {x: p, 'evidence':e}}       
    
    def print(self):
        """ Print on stdout the structure of the network.
        """

        print('Network:')
        for p,c in self.g.edges:
            print(' '+p+' -> '+c)
        
        # print nodes without edges
        for node in self.g.nodes:
            if self.g.out_degree(node) + self.g.in_degree(node) == 0: print(' '+node)

        print()

    def plot(self) -> graphviz:
        """ Plot the graph of the network.

        Returns:    
            graphviz: can be plotted automatically in jupyter notebook. 
        """

        # convert graph to graphviz
        A = nx.nx_agraph.to_agraph(self.g)
        A.layout('dot')

        # change color 
        for node in A.iternodes():
            node.attr['color'] = 'lightblue'
            node.attr['style'] = 'filled'
            node.attr['fontname'] = 'Futura'

        return A
    
