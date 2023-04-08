# Bayesian Network from scratch in python

I choose to implement the Bayesian Network in Python by writing a simple interface that allows the user to define its own custom network and run some experiments on it.

Bayesian Network is implemented by two classes: `BayesianNetwork` and `Bnode`. The first one is the main class that contains the network structure and the second one is the class that represents a single node in the network.

The `Bnode` class is defined as follows:

```python
    def __init__(self, cpt: dict, parents: list):
        self.cpt = cpt
        self.parents = parents
```

where `parents` is a list of the parents of the node and `cpt` is the conditional probability table of the node.

The `BayesianNetwork` class is defined as follows:

```python
    def __init__(self, nodes: dict, values: list):
        self.nodes = nodes
        self.values = values 
        G = nx.DiGraph(self.get_edges())

        # check acyclicity of graph
        if nx.is_directed_acyclic_graph(G): self.g = G
        else: raise ValueError('Network is not acyclic.')

        # add nodes without edges to the graph
        for node in self.get_nodes():
            if node not in self.g.nodes: self.g.add_node(node)

```
    
where `nodes` is a dictionary that maps the name of the node to the `Bnode` object, `values` is a list of the possible values of the nodes (e.g. `['T', 'F']`) and `g` is the *networkx* graph that represents the network structure. The constructor also checks if the network is acyclic and adds nodes without edges to the graph.

The `sampling()` method of `BayesianNetwork` class implement the Ancestral Sampling algorithm. It takes as input the number of samples to generate and returns a dictionary that maps the sample number to the sample itself. It allows also to specify an initial state of the network by adding some evidemce to the network. Also a seed can be specified for reproducibility.

```python
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
```

The `multi_choice()` method is a helper function that allows to sample from a multinomial or binomial distribution. It takes as input a list of possible values and a list of probabilities and returns a random value sampled from the distribution.

```python
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
``` 

The `BayesianNetwork` class also has the methods `get_nodes()` and `get_edges()` to get nodes and edges of the network and the method `plot()` to plot the Bayesian Network with the *graphviz* module.