from bayes_net import BayesNetwork
import pprint

Burglary = {'False': 0.999, 'True': 0.001}
Earthquake = {'False': 0.998, 'True': 0.002}
Alarm = {
    ('True', 'True', 'True'): 0.95,
    ('True', 'True', 'False'): 0.05,
    ('True', 'False', 'True'): 0.94,
    ('True', 'False', 'False'): 0.06,
    ('False', 'True', 'True'): 0.29,
    ('False', 'True', 'False'): 0.71,
    ('False', 'False', 'True'): 0.001,
    ('False', 'False', 'False'): 0.999
}

cpt = {'Burglary': Burglary, 'Earthquake': Earthquake, 'Alarm': Alarm}

bn = BayesNetwork([('Burglary','Alarm'),('Earthquake','Alarm')],cpt)

samples = bn.sample(5)
pprint.pprint(samples)
