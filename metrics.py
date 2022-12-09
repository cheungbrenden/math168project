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

def get_mean_degree(G):
    degrees = [d for n, d in G.degree()]
    mean_degree = sum(degrees) / len(degrees)
    return mean_degree

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


def top_eigenvector_centrality(G, x=1):
    # Compute the eigenvector centrality of the graph
    eigenvector_centrality = nx.eigenvector_centrality(G)

    # Sort the nodes based on their eigenvector centrality score
    sorted_nodes = sorted(eigenvector_centrality, key=eigenvector_centrality.get, reverse=True)

    # Return the x nodes with the best eigenvector centrality
    return [(node, eigenvector_centrality[node]) for node in sorted_nodes[:x]]


# 1.b Assortativity, WEIGHTED
def gini_coef(G):
    deg_dist = np.array(list(dict(G.degree(weight="num_of_flights")).values()))
    res = 0.0
    for i in deg_dist:
        res += np.abs(deg_dist - i).sum()
        # if res < 0:
            # print(res)
        # if np.abs(deg_dist - i).sum() < 0:
        #     print(np.abs(deg_dist - i).sum())
    return res / G.number_of_nodes() / deg_dist.sum() / 2


# 1.c Network efficiency
def calculate_network_efficiency(G):
    efficiency = 0
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                # Calculate the shortest path between the two nodes
                path = nx.shortest_path(G, node1, node2)
                # Calculate the length of the path
                path_length = len(path)
                # Update the total efficiency
                efficiency += 1 / path_length
    # Return the average efficiency
    return efficiency / (len(G.nodes()) * (len(G.nodes()) - 1))


# 1.d.i global clutering coef, UNWEIGHTED
def clustering_coef(G):
    return nx.average_clustering(G)  # , weight="num_of_flights")


# 1.d.ii average_shortest_path_length, UNWEIGHTED
def average_shortest_path_length(G):
    return nx.average_shortest_path_length(G)


# 1.e Scale Free Properties
def analyze_degree_distribution(G):
    # Compute the in-degree and out-degree centralities for each node
    indeg_centralities = nx.in_degree_centrality(G)
    outdeg_centralities = nx.out_degree_centrality(G)

    # Count the number of nodes with each in-degree and out-degree
    indeg_counts = Counter(dict(G.in_degree()).values())
    outdeg_counts = Counter(dict(G.out_degree()).values())

    # Compute the probability of a node having each in-degree and out-degree
    indeg_probs = {k: v / G.number_of_nodes() for k, v in indeg_counts.items()}
    outdeg_probs = {k: v / G.number_of_nodes() for k, v in outdeg_counts.items()}

    # Compute the cumulative in-degree and out-degree probabilities
    indeg_cumulative_probs = {}
    outdeg_cumulative_probs = {}
    cum_prob = 0.0
    for k in sorted(indeg_probs.keys(), reverse=True):
        cum_prob += indeg_probs[k]
        indeg_cumulative_probs[k] = cum_prob
    cum_prob = 0.0
    for k in sorted(outdeg_probs.keys(), reverse=True):
        cum_prob += outdeg_probs[k]
        outdeg_cumulative_probs[k] = cum_prob

    # Return the cumulative in-degree and out-degree probabilities
    return indeg_cumulative_probs, outdeg_cumulative_probs


# 2.a resilience of a given airport
# Note: it can take up to 6 minutes to compute this value
def resilience(G):
    # 1. Relative strength s_i
    return nx.average_node_connectivity(G)
