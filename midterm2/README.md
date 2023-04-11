# Bayesian Network from scratch in python

I choose to implement the Bayesian Network in Python by writing a simple interface that allows the user to define its own custom network and run some experiments on it.

Bayesian Network is implemented by two classes: `BayesianNetwork` and `Bnode`. The first one is the main class that contains the network structure and the second one is the class that represents a single node in the network.

`Bnode` class is defined as follows:

```python
    def __init__(self, cpt: dict, parents: list):
        self.cpt = cpt
        self.parents = parents
```

where `parents` is a list of the parents of the node and `cpt` is the conditional probability table of the node.

`BayesianNetwork` class is defined as follows:

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

`sampling()` method implement the **Ancestral Sampling algorithm**. It takes as input the number of samples to generate and returns a dictionary that maps the sample number to the sample itself. It allows also to specify an initial state of the network by adding some evidemce to the network. Also a seed can be specified for reproducibility.

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

`estimate()` method implement the **Rejection Sampling algorithm**. It takes as input the probabilities to estimate and the samplings from which compute. It returns a dict with the result of the estimation `P(X=x|e)`.

``` python
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
```

`multi_choice()` method is a helper function that allows to sample from a multinomial or binomial distribution. It takes as input a list of possible values and a list of probabilities and returns a random value sampled from the distribution.

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

`BayesianNetwork` class also has the methods `get_nodes()` and `get_edges()` to get nodes and edges of the network and the method `plot()` to plot the Bayesian Network with the *graphviz* module.

## Usage

``` python
from bayes_net import BayesNetwork
from bnode import Node
import pprint

burglary = Node(
    cpt= { 'p' : [0.5,0.5] },
    parents=None
)

earthquake = Node(
    cpt= { 'p' : [0.5,0.5] },
    parents=None
)

alarm = Node(
    cpt= {
        ('True', 'True'): [0.95,0.05],
        ('True', 'False'): [0.94,0.06],
        ('False', 'True'): [0.29,0.71],
        ('False', 'False'): [0.001,0.999]
    },
    parents=['Burglary','Earthquake']
)

bn = BayesNetwork({'Alarm': alarm, 'Burglary': burglary, 'Earthquake': earthquake}, values=['True','False'])

pp = pprint.PrettyPrinter(sort_dicts=False)
samples = bn.sampling(5, init={'Burglary': 'True'})
pp.pprint(samples)

bn.plot()
```

<img src="images/burglary.png" width="500">
