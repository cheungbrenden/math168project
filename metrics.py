from util import *


# 1.b Assortativity
def gini_coef(G):
    deg_dist = np.array(list(dict(G.degree(weight="num_of_flights")).values()))
    res = 0
    for i in deg_dist:
        res += np.abs(deg_dist - i).sum()
    return res / G.number_of_nodes() / deg_dist.sum()

