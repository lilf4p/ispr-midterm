# bayes network class
from graph import Graph
import numpy as np
import random

class BayesNetwork:
    """ Bayes network data structure, undirected by default.
    
    Attributes:
        net (list): list of (father, child) tuples representing conditional dependencies.
        cpt (dict): Dictionary of conditional probability tables.

    """
    def __init__(self, connections, cpt):
        self.net = Graph(connections, directed=True, acyclic=True)
        self.cpt = cpt
        if len(self.get_nodes()) < len(self.net.__nodes__()):
            raise ValueError('Missing CPT')

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.net)
    
    def choice(self, probability : int, seed : int) -> str:
        """ Return True or False according to a given probability.

            Args:
                probability (int): probability of True.
                seed (int): random seed to repeat same sampling.
        """
        if seed != None: random.seed(seed)
        if random.random() < probability: return 'True'
        else: return 'False'

    def get_nodes(self):
        return list(self.cpt.keys())

    def sample (self, n=1, init: dict = None, seed: int = None) -> dict:
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
        print(self.get_nodes())

        for iter in range(n):
            s = {} # i-esimo sample
            for node in self.get_nodes():
                # get value of P(node|parents(node))
                #print(node)
                cpt_node = self.cpt[node] # cpt of the current node
                #print(cpt_node)
                # get past choice of parents(node)  
                parents = self.net.get_parents(node)
                #print(parents)

                if len(parents) == 0: 
                    cpt_entry = 'True'
                else: 
                    cpt_entry = (*[s[key] for key in parents],'True') 

                #print(cpt_node[cpt_entry])

                # sample P(node|parents(node)) and add to current sampling
                s[node] = self.choice(cpt_node[cpt_entry], seed=seed)
                #print(s)
            
            # add current sampling to samples
            samples[iter] = s
        
        return samples
  


        
