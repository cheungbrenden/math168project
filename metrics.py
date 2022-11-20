from util import *


# 1.b Assortativity, WEIGHTED
def gini_coef(G):
    deg_dist = np.array(list(dict(G.degree(weight="num_of_flights")).values()))
    res = 0
    for i in deg_dist:
        res += np.abs(deg_dist - i).sum()
    return res / G.number_of_nodes() / deg_dist.sum()



# 1.d.i global clutering coef, UNWEIGHTED
def clustering_coef(G):
    return nx.average_clustering(G)#, weight="num_of_flights")

# 1.d.ii average_shortest_path_length, UNWEIGHTED
def average_shortest_path_length(G):
    return nx.average_shortest_path_length(G)

# 2.a resilience of a given airport
def resilience(G):
    # 1. Relative strength s_i
    s_i = np.array([])
    for i in G.nodes():
        temp = 0
        for j in G.neighbors(i):
            temp += G.get_edge_data(i,j, 'num_of_flights')['num_of_flights']
        s_i = np.append(s_i, temp)
    s_i_hat = s_i / s_i.sum()

    s_j_sum = s_i.sum()
    v_i = -2 * s_i + s_j_sum
    # R_i = 
