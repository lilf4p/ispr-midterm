# bayes network class
from graph import Graph
import numpy as np
import random
from node import Node
import networkx as nx
import matplotlib.pyplot as plt

# TODO: implement automatic graph generation - need to be acyclic 
# TODO: implement topological order of nodes
# TODO: implement graphical representation of network
# TODO: use graph networkx to do all the work on graph


class BayesNetwork:
    """ Bayes network data structure, undirected by default.
    
    Attributes:
        nodes (dict): Dictionary of nodes.
        values (list): List of values that each node can take. Ex: ['True', 'False'] for binomial, [0,1,2,3] for multinomial.

    """
    def __init__(self, nodes: dict, values: list):
        #self.net = Graph(connections, directed=True, acyclic=True)
        self.nodes = nodes
        self.values = values 
        G = nx.DiGraph()
        G.add_edges_from(self.get_edges())
        self.g = G

    def get_nodes(self):
        return list(self.nodes.keys())
    
    def get_edges(self):
        edges = []
        for key,node in self.nodes.items():
            if node.get_parents() != None:
                for parent in node.get_parents():
                    edges.append((parent,key))
        return edges
    
    def graph(self):
        g={}
        for e in self.get_edges():
            parent, child = e
            if parent in g:
                g[parent].append(child)
            else:
                g[parent] = [child]
        return g
        
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.net)
    
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

    def sampling (self, n=1, init: dict = None, seed: int = None) -> dict:
        """ Ancestral sampling n times from the network.
        
        Args:
            n (int): number of times to sample.
            init (dict): initial state of the network.
            seed (int): random seed.

        Returns:
            dict: n samples
        """
        init = init or {}
        samples={} # n samples

        # take nodes from the network

        # TODO: topological order of nodes
        nodes = list(nx.topological_sort(self.g))
        print(nodes)

        for iter in range(n):
            s = {} # i-esimo sample
            for n in nodes: # get node in topological order
                
                node = self.nodes[n]
                # get cpt of node
                cpt = node.get_cpt() # cpt of the current node
                
                # get parents of node
                parents = node.get_parents()

                if parents == None: 
                    s[n] = self.multi_choice(self.values, cpt['p'])
                else:
                    s[n] = self.multi_choice(self.values, cpt[tuple([s[parent] for parent in parents])])
                            
            # add current sampling to samples
            samples[iter] = s
        
        return samples
    
    def print_graph(self):
        print('Graph:')
        for key,val in self.graph().items():
            print(' '+key+' -> ', end='')
            for v in val:
                print(v, end=', ')
            print()
        print()

    def draw_graph(self):
        nx.draw(self.g, with_labels=True, font_weight='bold', node_size=5000, font_size=11)
        plt.show()