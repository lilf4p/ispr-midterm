class Bnode:

    def __init__(self, cpt: dict, parents: list):
        """Bayes network node data structure.

        Args:
            cpt (dict): Dictionary of conditional probability tables.
            parents (list): list of parents of each node.
        """ 

        self.cpt = cpt
        self.parents = parents

    def get_cpt(self):
        return self.cpt
    
    def get_parents(self):
        return self.parents
        
