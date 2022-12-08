import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.lines as mlines
import warnings

warnings.filterwarnings("ignore")


# Create Graph
def create_graph(data):
    """Create a graph given a cleanded pandas df

    Args:
        data: pandas df

    Returns:
        a directed, weighted graph, with weight with the name "num_of_flights"
    """
    data.columns = [i.lower() for i in data.columns]
    temp = data.groupby(["origin", "dest"]).sum().reset_index()
    return nx.from_pandas_edgelist(temp, source='origin', target='dest', edge_attr=['num_of_flights'],
                                   create_using=nx.DiGraph)


# Converts directed graph to undirected graph, summing edge values of A->B and B->A
def to_undirected_graph(G):
    # Create a new undirected graph
    H = nx.Graph()

    # Iterate over the edges in the original directed graph
    for u, v, w in G.edges(data='num_of_flights'):
        # Check if the edge from v to u exists in the original graph
        if (v, u) in G.edges():
            # If the edge exists, add it to the new undirected graph
            # with the num_of_flight equal to the sum of the num_of_flight
            # of the corresponding edges in the original directed graph
            H.add_edge(u, v, num_of_flights=w + G[v][u]['num_of_flights'])
        else:
            # If the edge does not exist, add it to the new undirected
            # graph with the num_of_flight equal to the num_of_flight
            # of the edge from u to v in the original directed graph
            H.add_edge(u, v, num_of_flights=w)

    # Return the new undirected graph
    return H


# Visualization
airports_us = pd.read_csv("data/airports_us.csv")
m = Basemap(
    projection='merc',
    llcrnrlon=-180,
    llcrnrlat=10,
    urcrnrlon=-50,
    urcrnrlat=65,
    lat_ts=0,
    resolution='l',
    suppress_ticks=True)
mx, my = m(airports_us['longitude'].values, airports_us['latitude'].values)
pos = {}
for count, elem in enumerate(airports_us['airport']):
    pos[elem] = (mx[count], my[count])


def viz_map(flights, year):
    """visualize flights data on a map

    Args:
        flights: a cleaned dataframe 
        year: just input a year, so it can make the right title and save with the correct file name
    """
    flights.columns = [i.lower() for i in flights.columns]

    plt.figure(figsize=(10, 9))
    temp = flights.groupby(["origin", "dest"]).sum().reset_index()
    counts = pd.DataFrame(temp.origin.value_counts())
    counts.columns = ["total_flight"]
    G_2009 = nx.from_pandas_edgelist(temp, source='origin', target='dest', edge_attr=['num_of_flights'],
                                     create_using=nx.DiGraph)
    # plt.figure(figsize=(15,20))
    nx.draw_networkx_nodes(G=G_2009, pos=pos, nodelist=[x for x in G_2009.nodes() if counts['total_flight'][x] >= 100],
                           node_color='#e74c3c', alpha=0.8,
                           node_size=[counts['total_flight'][x] * 4 for x in G_2009.nodes() if
                                      counts['total_flight'][x] >= 100])

    nx.draw_networkx_labels(G=G_2009, pos=pos, font_size=10,
                            labels={x: x for x in G_2009.nodes() if counts['total_flight'][x] >= 100})

    nx.draw_networkx_nodes(G=G_2009, pos=pos, nodelist=[x for x in G_2009.nodes() if counts['total_flight'][x] < 100],
                           node_color='#f7a503', alpha=0.6,
                           node_size=[counts['total_flight'][x] * 4 for x in G_2009.nodes() if
                                      counts['total_flight'][x] < 100])

    nx.draw_networkx_edges(G=G_2009, pos=pos, edge_color='#2D68C4', width=temp['num_of_flights'] * 0.00081,
                           alpha=0.1, arrows=False)

    m.drawcountries(linewidth=3)
    m.drawstates(linewidth=0.2)
    m.drawcoastlines(linewidth=1)
    m.fillcontinents(alpha=0.3)
    line1 = mlines.Line2D(range(1), range(1), color="white",
                          marker='o', markerfacecolor="#e74c3c")
    line2 = mlines.Line2D(range(1), range(1), color="white",
                          marker='o', markerfacecolor="#f7a503")
    line3 = mlines.Line2D(range(1), range(1), color="#2D68C4",
                          marker='', markerfacecolor="#2D68C4")
    plt.legend((line1, line2, line3), ('Large Airport >= 100 routes', 'Smaller airports', 'routes'))
    plt.title(f"Network graph of flight routes in the USA in {year}", fontsize=30)
    plt.tight_layout()
    plt.savefig(f"./images/{year}.jpg", format="jpg",
                dpi=300, bbox_inches="tight")
    plt.show()
