from util import *


# 1.a Centrality Measures


def airport_dict(G):
    """
    :param G:
    :return: dictionary(key = airport, value = index)
    """

    airports = [airport for airport in G.nodes]
    airports_dict = {k: v for v, k in enumerate(airports)}
    return airports_dict


def weighted_adjacency_matrix(G):
    """
    :param G: Graph
    :return: numpy matrix of 296x296

    note: there are 296 airports in the network
    """

    airports = [airport for airport in G.nodes]
    airports_dict = {k: v for v, k in enumerate(airports)}
    flight_matrix = []
    for airport in airports:
        current_airport_list = [0] * len(airports)
        for neighbor in list(G.neighbors(airport)):
            current_airport_list[airports_dict[neighbor]] = G.get_edge_data(airport, neighbor, 'num_of_flights')[
                'num_of_flights']
        flight_matrix.append(current_airport_list)
    np_flight_matrix = np.matrix(flight_matrix)

    return np_flight_matrix


def unweighted_adjacency_matrix(G):
    """
    :param G: Graph
    :return: numpy matrix of 296x296

    note: there are 296 airports in the network
    """

    airports = [airport for airport in G.nodes]
    airports_dict = {k: v for v, k in enumerate(airports)}
    flight_matrix = []
    for airport in airports:
        current_airport_list = [0] * len(airports)
        for neighbor in list(G.neighbors(airport)):
            current_airport_list[airports_dict[neighbor]] = 1
        flight_matrix.append(current_airport_list)
    np_flight_matrix = np.matrix(flight_matrix)

    return np_flight_matrix


def get_num_of_flights(G, origin, dest, weighted=True):
    airportsDict = airport_dict(G)
    adj_matrix = weighted_adjacency_matrix(G) if weighted else unweighted_adjacency_matrix(G)

    if not (origin in airportsDict and dest in airportsDict):
        return "Origin or Dest airport not in airports dictionary"
    return adj_matrix[airportsDict[origin], airportsDict[dest]]


def degrees(G, ascending=False, num_of_entries=None):
    """

    :param G: Graph
    :param ascending:
    True - lowest to highest
    (default) False - highest to lowest
    :param num_of_entries:
    (default) None - show all airports
    positive int x - show x airports
    :return: [(airport, degree)]
    """
    d = dict(G.degree(weight="num_of_flights"))
    return sorted(d.items(), key=lambda x: x[1], reverse=(not ascending))[:num_of_entries]


def betweenness_centrality(G, weighted=True, normalized=True, ascending=False, num_of_entries=None):
    """

    :param G: Graph
    :param weighted:
    (default) True - uses num_of_flights as edge weight
    False - no weight
    :param normalized:
    (default) True - betweenness value are normalized by 1/((n-1)(n-2))
    False - no normalization
    :param ascending:
    True - lowest to highest
    (default) False - highest to lowest
    :param num_of_entries:
    (default) None - show all airports
    positive int x - show x airports
    :return: [(airport, betweenness_centrality)]
    """

    bc_dict = nx.betweenness_centrality(G, weight="num_of_flights", normalized=normalized) if weighted else \
        nx.betweenness_centrality(G, normalized=normalized)

    return sorted(bc_dict.items(), key=lambda x: x[1], reverse=(not ascending))[:num_of_entries]



# 1.b Assortativity, WEIGHTED
def gini_coef(G):
    deg_dist = np.array(list(dict(G.degree(weight="num_of_flights")).values()))
    res = 0
    for i in deg_dist:
        res += np.abs(deg_dist - i).sum()
    return res / G.number_of_nodes() / deg_dist.sum()

# 1.c Network efficiency
def network_efficiency(G):
    pass


# 1.d.i global clutering coef, UNWEIGHTED
def clustering_coef(G):
    return nx.average_clustering(G)  # , weight="num_of_flights")


# 1.d.ii average_shortest_path_length, UNWEIGHTED
def average_shortest_path_length(G):
    return nx.average_shortest_path_length(G)

# 1.e Scale Free Properties
def power_law_dist(G):
    pass

# 2.a resilience of a given airport
def resilience(G):
    # 1. Relative strength s_i
    s_i = np.array([])
    for i in G.nodes():
        temp = 0
        for j in G.neighbors(i):
            temp += G.get_edge_data(i, j, 'num_of_flights')['num_of_flights']
        s_i = np.append(s_i, temp)
    s_i_hat = s_i / s_i.sum()

    s_j_sum = s_i.sum()
    v_i = -2 * s_i + s_j_sum
    # R_i =
