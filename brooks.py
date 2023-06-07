import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import collections

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


def vertex_with_less_than_max_degree(G):
    max_deg = max_degree(G)
    for node, degree in dict(G.degree()).items():
        if degree < max_deg:
            return node
    return None

def bfs_color(G, root):
    coloring = {}
    queue = collections.deque([(root, 0)])
    while queue:
        node, level = queue.popleft()
        # Assign color based on level
        coloring[node] = level % 2
        for neighbor in G[node]:
            if neighbor not in coloring:
                queue.append((neighbor, level + 1))
    return coloring

def greedy_draw_graph(G):
    # Choose a root node
    root = list(G.nodes())[0]

    # Color the nodes using BFS coloring
    coloring = bfs_color(G, root)

    # Get the number of colors used in the coloring
    num_colors = max(coloring.values()) + 1

    # Create a colormap with enough colors
    colormap = cm.get_cmap('viridis', num_colors)

    # Assign the colors to the nodes based on the coloring
    node_colors = [colormap(coloring[node]) for node in G.nodes()]

    nx.draw(G, with_labels=True, node_color=node_colors)
    plt.show()


def main():
    G = nx.Graph()

    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(4, 2)
    G.add_edge(4, 3)
    G.add_edge(1, 5)
    G.add_edge(1, 5)
    G.add_edge(5, 6)
    G.add_edge(1, 6)

    if is_complete(G) or has_odd_cycle(G):
        raise Exception("the graph is complete or contains an odd cycle")

    if max_degree(G) <= 2:
        # Find a valid coloring
        coloring = nx.coloring.greedy_color(G)
        colors = ['red', 'blue']

        for node in coloring:
            G.nodes[node]['color'] = colors[coloring[node]]

        node_colors = [nx.get_node_attributes(
            G, 'color')[node] for node in G.nodes()]
        nx.draw(G, with_labels=True, node_color=node_colors)
        plt.show()

    else:
        vertex = vertex_with_less_than_max_degree(G)
        if vertex is not None:
            T = nx.bfs_tree(G, vertex)
            greedy_draw_graph(T)  

    print(f"The maximum degree in the graph is: {max_degree(G)}")
    print(f"The graph is connected: {is_connected(G)}")


if __name__ == "__main__":
    main()
