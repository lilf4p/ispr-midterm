from bayes_net import BayesNetwork, Node 
import numpy as np
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
# from the given input BN class can construct the entire BN structure

bn.print_graph()

pp = pprint.PrettyPrinter(sort_dicts=False)
samples = bn.sampling(5)
pp.pprint(samples)

bn.draw_graph()

