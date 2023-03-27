# bayes network class

from graph import Graph

class BayesNetwork:
    """ Bayes network data structure, undirected by default.
    
    Attributes:
        net (list): list of (father, child) tuples representing conditional dependencies.
        cpt (dict): Dictionary of conditional probability tables.

    """
    def __init__(self, connections, cpt):
        self.net = Graph(connections, directed=True, acyclic=True)
        self.cpt = cpt

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.net)
    
    def sample (self, n=1, init: dict = None, seed: int = None):
        """ Ancestral sampling n times from the network.
        
        Args:
            n (int): number of times to sample.
            init (dict): initial state of the network.
            seed (int): random seed.
        """
        init = init or {}
        sample={}

        for iter in range(n):
            for node in self.net.__nodes__():
            # access P(node|parents(node))
                print(node)
                cpt_node = self.cpt[node]
                print(cpt_node)

        
