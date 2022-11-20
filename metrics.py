from util import *


# Metrics
def gini_coef(G):
    deg_dist = np.array(list(dict(G.degree(weight="num_of_flights")).values()))
    res = 0
    for i in deg_dist:
        res += np.abs(deg_dist - i).sum()