import networkx as nx
import matplotlib.pyplot as plt


def is_connected(G):
    return nx.is_connected(G)


def has_odd_cycle(G):
    for node in G.nodes():
        cycle = nx.find_cycle(G, source=node)
        if len(cycle) % 2 == 1:
            return True
    return False


def is_complete(G):
    num_nodes = len(G.nodes())
    num_edges = len(G.edges())
    max_edges = (num_nodes * (num_nodes - 1))
    return num_edges == max_edges


def max_degree(G):
    return max(dict(G.degree()).values())


def main():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    G.add_edge(6, 1)


    if is_complete(G) or has_odd_cycle(G):
        raise Exception("the graph is complete or contains an odd cycle")

    if max_degree(G) <= 2:
        # Find a valid coloring
        coloring = nx.coloring.greedy_color(G)
        colors = ['red', 'blue']  # Define as many colors as you need

        # Assign the colors to the nodes based on the coloring
        for node in coloring:
            G.nodes[node]['color'] = colors[coloring[node]]

        node_colors = [nx.get_node_attributes(G, 'color')[node] for node in G.nodes()]
        nx.draw(G, with_labels=True, node_color=node_colors)
        plt.show()
        
        
    print(f"The maximum degree in the graph is: {max_degree(G)}")
    print(f"The graph is connected: {is_connected(G)}")

if __name__ == "__main__":
    main()